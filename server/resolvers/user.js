import {
  AuthenticationError,
  ForbiddenError,
  UserInputError
} from 'apollo-server-lambda'
import moment from 'moment'
import crypto from 'crypto'
import { AdvitoUser, AdvitoUserSession, AccessToken } from '../models'
import {
  saltHash,
  generateAccessToken,
  getExpirationDate,
  sendEmail,
  checkValidPassword
} from '../utils'
import {
  SESSION,
  ADVITO_INGESTION_APPLICATION,
  EMAIL_TEMPLATE,
  EMAIL_URL,
  RECOVERY
} from '../constants'

export const user = {
  Mutation: {
    login: async (_, { username, password }) => {
      const user = await AdvitoUser.query()
        .where('username', username.toLowerCase())
        .first()
      if (!user) throw new UserInputError('User not found')
      if (!user.isEnabled) throw new UserInputError('User is not enabled')
      const { pwd: dbPassword, userSalt } = user
      const { passwordHashed } = saltHash(password, userSalt)
      if (dbPassword !== passwordHashed) {
        throw new UserInputError('Password is incorrect')
      }
      const roleLinkList = await user.$relatedQuery('advitoUserRoleLink')
      const roleIds = roleLinkList.map(role => role.advitoRoleId)
      const session = await user
        .$relatedQuery('advitoUserSession')
        .where('sessionEnd', null)
        .first()
      if (session) {
        await user
          .$relatedQuery('advitoUserSession')
          .patch({
            sessionEnd: moment.utc()
          })
          .where('sessionEnd', null)
      }
      const sessionToken = crypto.randomBytes(16).toString('base64')
      const date = moment.utc()
      await user.$relatedQuery('advitoUserSession').insert({
        sessionToken: sessionToken,
        sessionStart: date,
        sessionEnd: null,
        sessionDurationSec: 3600,
        sessionType: 'A3 User',
        sessionExpiration: getExpirationDate(SESSION),
        sessionNote: null,
        created: date,
        modified: date
      })
      await user.$relatedQuery('advitoUserLog').insert({
        advitoUserId: user.id,
        activity: 'User login'
      })

      return {
        id: user.id,
        displayName: user.fullName(),
        clientId: user.clientId,
        profilePicturePath: user.profilePicturePath,
        sessionToken,
        roleIds
      }
    },
    logout: async (_, { sessionToken }) => {
      const session = await AdvitoUserSession.query()
        .where('sessionToken', sessionToken)
        .where('sessionEnd', null)
        .first()
      if (!session) throw new AuthenticationError('User session not found')
      await AdvitoUserSession.query()
        .patch({
          sessionEnd: moment.utc()
        })
        .where('sessionToken', sessionToken)
        .where('sessionEnd', null)
      return true
    },
    sendResetPasswordEmail: async (_, { email }) => {
      const user = await AdvitoUser.query()
        .where('email', email.toLowerCase())
        .first()
      if (!user) throw new UserInputError('User not found')
      const oldToken = await user
        .$relatedQuery('accessToken')
        .where('isActive', true)
        .first()
      if (oldToken) {
        await user
          .$relatedQuery('accessToken')
          .patch({ isActive: false })
          .where('isActive', true)
          .first()
      }
      const token = generateAccessToken('PASS')
      await user.$relatedQuery('accessToken').insert({
        tokenType: 'RECOVERY',
        token,
        tokenExpiration: getExpirationDate(RECOVERY)
      })
      const placeholders = {
        NAMEFIRST: user.nameFirst,
        URL: `${EMAIL_URL}${token}`
      }
      try {
        await sendEmail(
          EMAIL_TEMPLATE,
          user.email,
          placeholders,
          ADVITO_INGESTION_APPLICATION
        )
        await user.$relatedQuery('advitoUserLog').insert({
          advitoUserId: user.id,
          activity: 'User sent reset password email'
        })
        return `Password has been sent to ${user.email}`
      } catch (err) {
        throw new ForbiddenError(err.message)
      }
    },
    resetPassword: async (_, { token, password, confirmPassword }) => {
      if (password !== confirmPassword) {
        throw new UserInputError('Passwords do not match')
      }
      const errorMessages = checkValidPassword(password)
      if (errorMessages.length) throw new UserInputError(errorMessages)
      const accessToken = await AccessToken.query()
        .where('token', token)
        .first()
      if (!accessToken) {
        throw new AuthenticationError('Access token is not valid')
      }
      const { isActive, tokenExpiration, advitoUserId } = accessToken
      if (!isActive || tokenExpiration < moment.utc()) {
        throw new AuthenticationError('Access token is not valid')
      }
      const { saltHashed, passwordHashed } = saltHash(password)
      const user = await AdvitoUser.query().patchAndFetchById(advitoUserId, {
        pwd: passwordHashed,
        userSalt: saltHashed
      })
      await user.$relatedQuery('advitoUserLog').insert({
        advitoUserId: user.id,
        activity: 'User password reset'
      })
      return true
    }
  }
}

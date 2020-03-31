import { ApolloError } from 'apollo-server-lambda'
import { AdvitoUserSession } from './models'
import moment from 'moment'

export const authenticateUser = async (sessionToken, advitoDb) => {
	if (!sessionToken) return null
	const session = await AdvitoUserSession.query(advitoDb)
		.where('sessionToken', sessionToken)
		.andWhere('sessionEnd', null)
		.first()
	if (!session) throw new ApolloError('Session is invalid.', 401)

	const { id, sessionExpiration, sessionDurationSec } = session

	if (sessionExpiration <= moment.utc()) {
		throw new ApolloError('Session has expired.', 401)
	}
	const newExpiration = moment.utc().add(sessionDurationSec, 's')
	const timeDifference = newExpiration.diff(sessionExpiration, 'm')
	if (timeDifference > 50) {
		try {
			await AdvitoUserSession.query(advitoDb).patchAndFetchById(id, {
				sessionExpiration: newExpiration
			})
		} catch (err) {
			console.log(err)
		}
	}

	const user = await session.$relatedQuery('advitoUser', advitoDb).first()
	if (!user) throw new ApolloError('User not found', 401)
	const roleLinkList = await user.$relatedQuery('advitoUserRoleLink', advitoDb)
	const roleIds = roleLinkList.map(role => role.advitoRoleId)
	return {
		...user,
		name: user.fullName(),
		roleIds
	}
}

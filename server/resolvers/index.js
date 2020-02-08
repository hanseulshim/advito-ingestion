import { GraphQLScalarType } from 'graphql'
import { Kind } from 'graphql/language'
import merge from 'lodash/merge'
import user from './user'
import client from './client'
import application from './application'
import moment from 'moment'

export const resolvers = {
  ...merge(
    user,
    client,
    application
  ),
  Date: new GraphQLScalarType({
    name: 'Date',
    description: 'Date custom scalar type',
    parseValue(value) {
      return moment.utc(value)
    },
    serialize(value) {
      return moment.utc(value).valueOf()
    },
    parseLiteral(ast) {
      if (ast.kind === Kind.INT) {
        return parseInt(ast.value, 10)
      }
      return null
    }
  })
}

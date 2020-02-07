import { gql } from 'apollo-server-lambda'
import { user } from './user'

export const typeDefs = gql`
  scalar Date
  directive @auth on FIELD_DEFINITION
  ${user}
  type Query {
    _empty: String
  }
  type Mutation {
    _empty: String
  }
`

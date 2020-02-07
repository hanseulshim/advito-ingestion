import { gql } from 'apollo-server-lambda'
import { user } from './user'
import { client } from './client'

export const typeDefs = gql`
  scalar Date
  directive @auth on FIELD_DEFINITION
  ${user}
  ${client}
  type Query {
    _empty: String
  }
  type Mutation {
    _empty: String
  }
`

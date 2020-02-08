import { gql } from 'apollo-server-lambda'
import user from './user'
import client from './client'
import application from './application'

export const typeDefs = gql`
  scalar Date
  directive @auth on FIELD_DEFINITION
  ${user}
  ${client}
  ${application}
  type Query {
    _empty: String
  }
  type Mutation {
    _empty: String
  }
`

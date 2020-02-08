import user from './user'
import client from './client'
import application from './application'

export default {
  tabs: [user.Mutation, client.Query, application.Query]
}

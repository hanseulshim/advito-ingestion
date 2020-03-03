import user from './user'
import client from './client'
import application from './application'
import upload from './upload'

export default {
	tabs: [user.Mutation, client.Query, application.Query, upload.Query]
}

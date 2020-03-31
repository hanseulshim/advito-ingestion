import { ApolloServer } from 'apollo-server-lambda'
import { typeDefs } from './typeDefs'
import { resolvers } from './resolvers'
import requireAuthDirective from './directives'
import playground from './playground'
import { authenticateUser } from './helper'
import Knex from 'knex'
import { Model, knexSnakeCaseMappers } from 'objection'

const db = Knex({
	client: 'pg',
	connection: {
		host: process.env.DB_HOST,
		user: process.env.DB_USER,
		password: process.env.DB_PASSWORD,
		database: process.env.ADVITO_DB_DATABASE
	},
	...knexSnakeCaseMappers()
})
Model.knex(db)

const server = new ApolloServer({
	typeDefs,
	resolvers,
	context: async ({ event }) => {
		const sessionToken = event.headers.sessiontoken || ''
		const user = await authenticateUser(sessionToken)
		return { user }
	},
	schemaDirectives: {
		auth: requireAuthDirective
	},
	playground
})

export const graphqlHandler = server.createHandler({
	cors: {
		origin: true,
		credentials: true
	}
})

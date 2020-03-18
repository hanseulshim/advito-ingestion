import { ADVITO_CLIENT_ID } from '../constants'
import { Client } from '../models'

export default {
	Query: {
		clientList: async (_, __, { user }) => {
			if (parseInt(user.clientId) === ADVITO_CLIENT_ID) {
				return Client.query()
					.where('isActive', true)
					.orderBy('clientName')
			} else {
				return Client.query().where('id', user.clientId)
			}
		}
	}
}

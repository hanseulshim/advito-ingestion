import { Client, AdvitoApplicationRole } from '../models'

export default {
	Query: {
		clientList: async (_, __, { user }) => {
			const applicationIds = await AdvitoApplicationRole.query()
				.whereIn('id', user.roleIds)
				.distinct('advitoApplicationId')

			return Client.query()
				.alias('c')
				.skipUndefined()
				.distinct('c.id', 'c.clientName')
				.leftJoinRelated('applications as a')
				.whereIn(
					'a.id',
					applicationIds.map(i => i.advitoApplicationId)
				)
				.where('c.isActive', true)
				.orderBy('c.clientName')
		}
	}
}

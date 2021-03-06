import {
	AdvitoApplication,
	AdvitoApplicationTemplate,
	AdvitoApplicationTemplateSource
} from '../models'

export default {
	Query: {
		applicationList: async (_, __, { user }) =>
			AdvitoApplication.query()
				.select('a.id', 'a.applicationName')
				.alias('a')
				.leftJoin(
					'advitoApplicationRole as ar',
					'ar.advitoApplicationId',
					'a.id'
				)
				.leftJoin('advitoUserRoleLink as ur', 'ur.advitoRoleId', 'ar.id')
				.leftJoin('advitoUser as u', 'u.id', 'ur.advitoUserId')
				.where('u.id', user.id)
				.andWhere('a.isActive', true),
		practiceAreaList: async (_, { clientId }, { user }) =>
			AdvitoApplication.query()
				.select('a.id', 'a.applicationName')
				.alias('a')
				.leftJoin(
					'clientAdvitoApplicationLink as c',
					'c.advitoApplicationId',
					'a.id'
				)
				.leftJoin(
					'advitoApplicationRole as ar',
					'ar.advitoApplicationId',
					'a.id'
				)
				.leftJoin('advitoUserRoleLink as ur', 'ur.advitoRoleId', 'ar.id')
				.leftJoin('advitoUser as u', 'u.id', 'ur.advitoUserId')
				.where('c.clientId', clientId)
				.andWhere('u.id', user.id)
				.andWhere('a.isActive', true),
		templateList: async (_, { applicationId }) =>
			await AdvitoApplicationTemplate.query()
				.select('t.*', 'a.application_name')
				.alias('t')
				.leftJoin('advitoApplication as a', 'a.id', 't.advitoApplicationId')
				.where('advitoApplicationId', applicationId)
				.orderBy('t.sequence'),
		sampleTemplateList: async (_, __, { user }) =>
			AdvitoApplicationTemplate.query()
				.select('t.*', 'a.application_name')
				.alias('t')
				.leftJoin('advitoApplication as a', 'a.id', 't.advitoApplicationId')
				.leftJoin(
					'advitoApplicationRole as ar',
					'ar.advitoApplicationId',
					'a.id'
				)
				.leftJoin('advitoUserRoleLink as ur', 'ur.advitoRoleId', 'ar.id')
				.leftJoin('advitoUser as u', 'u.id', 'ur.advitoUserId')
				.where('u.id', user.id)
				.andWhere('a.isActive', true)
				.orderBy(['a.application_name', 't.sequence']),
		sourceList: async (_, { templateId }) =>
			AdvitoApplicationTemplateSource.query()
				.where('advitoApplicationTemplateId', templateId)
				.orderBy('sequence')
	}
}

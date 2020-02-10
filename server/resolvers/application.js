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
    templateList: async (_, { applicationId }) =>
      await AdvitoApplicationTemplate.query()
        .select('t.*', 'a.application_name')
        .alias('t')
        .leftJoin('advitoApplication as a', 'a.id', 't.advitoApplicationId')
        .where('advitoApplicationId', applicationId),
    sourceList: async (_, { templateId }) =>
      AdvitoApplicationTemplateSource.query().where(
        'advitoApplicationTemplateId',
        templateId
      )
  }
}

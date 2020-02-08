import { Model } from 'objection'

export class Client extends Model {
  static get tableName() {
    return 'client'
  }

  static get relationMappings() {
    const { AdvitoApplication } = require('./application')
    return {
      applications: {
        relation: Model.ManyToManyRelation,
        modelClass: AdvitoApplication,
        join: {
          from: 'client.id',
          through: {
            from: 'clientAdvitoApplicationLink.clientId',
            to: 'clientAdvitoApplicationLink.advitoApplicationId'
          },
          to: 'advitoApplication.id'
        }
      }
    }
  }
}

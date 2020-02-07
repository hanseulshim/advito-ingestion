import { ADVITO_CLIENT_ID, ADVITO_INGESTION_APPLICATION } from '../constants'
import { Client } from '../models'

export const client = {
  Query: {
    clientList: async (_, __, { user }) => {
      if (parseInt(user.clientId) === ADVITO_CLIENT_ID) {
        return Client.query()
        .alias('c')
        .joinRelated('applications', {alias: 'a'})
        .where('a.id', ADVITO_INGESTION_APPLICATION)
        .andWhere('c.isActive', true);
      } else {
        return Client.query().where('id', user.clientId)
      }
    }
  }
}

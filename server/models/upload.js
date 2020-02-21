import { Model } from 'objection'

export class JobIngestion extends Model {
  static get tableName() {
    return 'jobIngestion'
  }
}

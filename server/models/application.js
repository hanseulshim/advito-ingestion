import { Model } from 'objection'

export class AdvitoApplication extends Model {
  static get tableName() {
    return 'advitoApplication'
  }
}

export class AdvitoApplicationRole extends Model {
  static get tableName() {
    return 'advitoApplicationRole'
  }
}
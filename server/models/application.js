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

export class AdvitoApplicationTemplate extends Model {
  static get tableName() {
    return 'advitoApplicationTemplate'
  }
}

export class AdvitoApplicationTemplateSource extends Model {
  static get tableName() {
    return 'advitoApplicationTemplateSource'
  }
}

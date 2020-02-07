import { Model } from 'objection'

export class AdvitoUser extends Model {
  static get tableName() {
    return 'advitoUser'
  }

  name() {
    return this.nameFirst + ' ' + this.nameLast
  }

  fullName() {
    return this.nameFirst + ' ' + this.nameLast
  }

  static get relationMappings() {
    return {
      advitoUserRoleLink: {
        relation: Model.HasManyRelation,
        modelClass: AdvitoUserRoleLink,
        join: {
          from: 'advitoUser.id',
          to: 'advitoUserRoleLink.advitoUserId'
        }
      },
      advitoUserSession: {
        relation: Model.HasManyRelation,
        modelClass: AdvitoUserSession,
        join: {
          from: 'advitoUser.id',
          to: 'advitoUserSession.advitoUserId'
        }
      },
      accessToken: {
        relation: Model.HasManyRelation,
        modelClass: AccessToken,
        join: {
          from: 'advitoUser.id',
          to: 'accessToken.advitoUserId'
        }
      },
      advitoUserLog: {
        relation: Model.HasManyRelation,
        modelClass: AdvitoUserLog,
        join: {
          from: 'advitoUser.id',
          to: 'advitoUserLog.advitoUserId'
        }
      }
    }
  }
}

export class AdvitoUserRoleLink extends Model {
  static get tableName() {
    return 'advitoUserRoleLink'
  }
}

export class AdvitoUserSession extends Model {
  static get tableName() {
    return 'advitoUserSession'
  }

  static get relationMappings() {
    return {
      advitoUser: {
        relation: Model.HasManyRelation,
        modelClass: AdvitoUser,
        join: {
          from: 'advitoUserSession.advitoUserId',
          to: 'advitoUser.id'
        }
      }
    }
  }
}

export class AccessToken extends Model {
  static get tableName() {
    return 'accessToken'
  }
}

export class EmailTemplate extends Model {
  static get tableName() {
    return 'emailTemplate'
  }
}

export class AdvitoUserLog extends Model {
  static get tableName() {
    return 'advitoUserLog'
  }

  static get relationMappings() {
    return {
      advitoUser: {
        relation: Model.HasManyRelation,
        modelClass: AdvitoUser,
        join: {
          from: 'advitoUserLog.advitoUserId',
          to: 'advitoUser.id'
        }
      }
    }
  }
}

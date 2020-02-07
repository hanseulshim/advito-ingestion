import { SchemaDirectiveVisitor, ApolloError } from 'apollo-server-lambda'

export default class RequireAuthDirective extends SchemaDirectiveVisitor {
  visitFieldDefinition(field) {
    const { resolve = this.defaultFieldResolver } = field
    field.resolve = async (...args) => {
      const [, , context] = args
      if (context.user) {
        // const roleIds = context.user.roleIds.map(role => parseInt(role))
        // const idExists = IA_ROLES.some(role => roleIds.indexOf(role) >= 0)
        // if (!idExists) { throw new ApolloError('User did not have I&A role', 401) }
        const result = await resolve.apply(this, args)
        return result
      } else {
        throw new ApolloError(
          'You must be signed in to view this resource.',
          401
        )
      }
    }
  }
}

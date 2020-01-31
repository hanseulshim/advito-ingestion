import gql from 'graphql-tag'

export const APPLICATION_LIST = gql`
  {
    applicationList {
      applicationName
      enabled
    }
  }
`
export const ANALYTICS_ID = 3

import gql from 'graphql-tag'

export const CLIENT_LIST = gql`
  {
    clientList {
      id
      clientName
    }
  }
`

export const PRACTICE_AREA_LIST = gql`
  query practiceAreaList($clientId: Int) {
    practiceAreaList(clientId: $clientId) {
      id
      applicationName
    }
  }
`

export const TEMPLATE_LIST = gql`
  query templateList($applicationId: Int) {
    templateList(applicationId: $applicationId) {
      id
      templateName
    }
  }
`

export const SOURCE_LIST = gql`
  query sourceList($templateId: Int) {
    sourceList(templateId: $templateId) {
      id
      sourceName
    }
  }
`

export const APPLICATION_LIST = gql`
  {
    applicationList {
      id
      applicationName
    }
  }
`
export const SAMPLE_TEMPLATE_LIST = gql`
  {
    sampleTemplateList {
      id
      templateName
      applicationName
      templatePath
    }
  }
`

export const ANALYTICS_ID = 3

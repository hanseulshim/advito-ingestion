import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import * as serviceWorker from './serviceWorker'
import { Router } from 'react-router-dom'
import history from './history'
import { fetch } from 'isomorphic-unfetch'
import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  ApolloLink,
  HttpLink,
  from
} from '@apollo/client'
import { onError } from '@apollo/link-error'
import { getToken, removeUser, getApi } from './helper'

const errorLink = onError(({ graphQLErrors }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ extensions }) => {
      if (extensions.code === 401) {
        removeUser()
      }
    })
  }
})

const authMiddleware = new ApolloLink((operation, forward) => {
  const sessiontoken = getToken()
  if (sessiontoken) {
    operation.setContext({
      headers: {
        sessiontoken
      }
    })
  }
  return forward(operation)
})

const httpLink = new HttpLink({
  uri: getApi()
})

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: from([errorLink, authMiddleware, httpLink]),
  fetchOptions: { fetch }
})

ReactDOM.render(
  <ApolloProvider client={client}>
    <Router history={history}>
      <App />
    </Router>
  </ApolloProvider>,
  document.getElementById('root')
)

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister()

import React from 'react'
import PropTypes from 'prop-types'
import { ThemeProvider } from 'styled-components'
import { Route, Switch, Redirect } from 'react-router-dom'
import theme from 'styles/variables'
import GlobalStyle from 'styles/GlobalStyle'
import Login from 'components/login'
import { getToken } from 'helper'
import Main from 'components/main'
import ResetPassword from 'components/login/ResetPassword'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

library.add(fas)

const PrivateRoute = ({ component: Component }) => (
  <Route render={() => (getToken() ? <Component /> : <Redirect to="/" />)} />
)

const App = () => (
  <ThemeProvider theme={theme}>
    <GlobalStyle />
    <Switch>
      <Route path="/login" component={Login} />
      <Route path="/reset-password" component={ResetPassword} />
      <PrivateRoute path="/" exact component={Main} />
    </Switch>
  </ThemeProvider>
)

PrivateRoute.propTypes = {
  component: PropTypes.func.isRequired
}

export default App

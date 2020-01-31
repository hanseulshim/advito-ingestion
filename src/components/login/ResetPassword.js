import React from 'react'
import PropTypes from 'prop-types'
import styled from 'styled-components'
import { Form, Icon, Input, Button } from 'antd'
import { useHistory, useLocation } from 'react-router'
import { useMutation } from '@apollo/react-hooks'
import queryString from 'query-string'
import advitoLogo from 'assets/advitoLogo.png'
import Footer from './Footer'
import { RESET_PASSWORD } from 'api'
import ErrorMessage from 'components/common/ErrorMessage'
import SuccessMessage from 'components/common/SuccessMessage'
import Loader from 'components/common/Loader'

const Container = styled.div`
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: ${props => props.theme.jungleMist};
`

const Logo = styled.img`
  margin: 3em 0 0 5em;
  max-width: 200px;
  width: 100%;
  align-self: flex-start;
`

const FormContainer = styled.div`
  padding: 2em 4em;
  width: 30%;
  max-width: 500px;
`

const Title = styled.div`
  font-size: 4em;
  text-align: center;
  margin: 2.5em 0 0.5em 0;
  color: ${props => props.theme.white};
`
const ButtonRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;
`

const Link = styled.div`
  color: ${props => props.theme.white};
  cursor: pointer;
  :hover {
    opacity: 0.7;
  }
`

const RestPassword = ({ form }) => {
  const history = useHistory()
  const location = useLocation()
  const [resetPassword, { loading, error, data }] = useMutation(RESET_PASSWORD)
  const params = queryString.parse(location.search)
  const { t: token = '' } = params

  const handleSubmit = e => {
    e.preventDefault()
    form.validateFields(async (err, { password, confirmPassword }) => {
      if (!err) {
        try {
          await resetPassword({
            variables: { password, confirmPassword, token }
          })
        } catch (e) {
          console.error('Error in reset password form: ', e)
        }
      }
    })
  }

  const { getFieldDecorator } = form
  return (
    <Container>
      <Logo src={advitoLogo} />
      <Title>Reset Password</Title>
      <FormContainer>
        <Form onSubmit={handleSubmit}>
          {loading ? (
            <Loader />
          ) : (
            <>
              <Form.Item>
                {getFieldDecorator('password', {
                  rules: [
                    { required: true, message: 'Please input your password!' }
                  ]
                })(
                  <Input
                    prefix={
                      <Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />
                    }
                    type="password"
                    placeholder="Password"
                  />
                )}
              </Form.Item>
              <Form.Item>
                {getFieldDecorator('confirmPassword', {
                  rules: [
                    { required: true, message: 'Please input your password!' }
                  ]
                })(
                  <Input
                    prefix={
                      <Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />
                    }
                    type="password"
                    placeholder="Confirm Password"
                  />
                )}
              </Form.Item>
            </>
          )}
          <Form.Item>
            <ButtonRow>
              <Button type="danger" htmlType="submit">
                Reset Password
              </Button>
              <Link onClick={() => history.push('/login')}>Back to Login</Link>
            </ButtonRow>
            {error && <ErrorMessage error={error} />}
            {data && <SuccessMessage message={'Password has been reset'} />}
          </Form.Item>
        </Form>
      </FormContainer>
      <Footer />
    </Container>
  )
}

const RestPasswordForm = Form.create({ name: 'restPassword' })(RestPassword)

RestPassword.propTypes = {
  form: PropTypes.object.isRequired
}

export default RestPasswordForm

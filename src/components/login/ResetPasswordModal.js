import React from 'react'
import PropTypes from 'prop-types'
import { useMutation } from '@apollo/react-hooks'
import { Modal, Form, Input, Button } from 'antd'
import { SEND_RESET_PASSWORD, ANALYTICS_ID } from 'api'
import ErrorMessage from 'components/common/ErrorMessage'
import SuccessMessage from 'components/common/SuccessMessage'
import Loader from 'components/common/Loader'

const ResetPasswordModal = ({ form, visible, setVisible }) => {
  const [sendResetPasswordEmail, { loading, error, data }] = useMutation(
    SEND_RESET_PASSWORD
  )

  const handleSubmit = event => {
    event.preventDefault()
    form.validateFields(async (err, { email }) => {
      if (!err) {
        try {
          await sendResetPasswordEmail({
            variables: { appId: ANALYTICS_ID, email }
          })
        } catch (e) {
          console.error('Error in reset password form: ', e)
        }
      }
    })
  }
  const { getFieldDecorator } = form

  return (
    <>
      <Modal
        title="Forgot Password"
        visible={visible}
        footer={null}
        onCancel={() => setVisible(false)}
      >
        <Form onSubmit={handleSubmit}>
          <div>Enter your email address below to reset your password</div>
          {loading ? (
            <Loader />
          ) : (
            <Form.Item>
              {getFieldDecorator('email', {
                rules: [
                  { required: true, message: 'Please input your email!' },
                  {
                    type: 'email',
                    message: 'The input is not a valid email!'
                  }
                ]
              })(<Input placeholder="Email" />)}
            </Form.Item>
          )}
          <Form.Item>
            <Button type="danger" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
          {error && <ErrorMessage error={error} />}
          {data && <SuccessMessage message={data.sendResetPasswordEmail} />}
        </Form>
      </Modal>
    </>
  )
}

const WrappedResetPasswordForm = Form.create({ name: 'reset_password' })(
  ResetPasswordModal
)

ResetPasswordModal.propTypes = {
  form: PropTypes.object.isRequired,
  visible: PropTypes.bool.isRequired,
  setVisible: PropTypes.func.isRequired
}

export default WrappedResetPasswordForm

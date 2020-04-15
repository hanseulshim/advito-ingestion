import React from 'react'
import { useMutation } from '@apollo/client'
import { Modal, Form, Input, Button } from 'antd'
import { SEND_RESET_PASSWORD } from 'api'
import ErrorMessage from 'components/common/ErrorMessage'
import SuccessMessage from 'components/common/SuccessMessage'
import { SkeletonLoader } from 'components/common/Loader'
import { authClient } from 'index'

const ResetPasswordModal = ({ form, visible, setVisible }) => {
	const [sendResetPasswordEmail, { loading, error, data }] = useMutation(
		SEND_RESET_PASSWORD,
		{
			client: authClient
		}
	)

	const handleSubmit = async ({ email }) => {
		try {
			await sendResetPasswordEmail({
				variables: { email }
			})
		} catch (e) {
			console.error('Error in reset password form: ', e)
		}
	}

	return (
		<>
			<Modal
				title="Forgot Password"
				visible={visible}
				footer={null}
				onCancel={() => setVisible(false)}
			>
				<Form onFinish={handleSubmit}>
					<div>Enter your email address below to reset your password</div>
					{loading ? (
						<SkeletonLoader />
					) : (
						<Form.Item
							name="email"
							rules={[
								{ required: true, message: 'Please input your email!' },
								{
									type: 'email',
									message: 'The input is not a valid email!'
								}
							]}
						>
							<Input placeholder="Email" />
						</Form.Item>
					)}
					<Form.Item name="submit">
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

export default ResetPasswordModal

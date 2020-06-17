import React from 'react'
import styled from 'styled-components'

const Title = styled.div`
	font-weight: 400;
	text-decoration: underline;
`

export const getSectionText = (key, text) => {
	if (key === 'unmaskedCreditCardData') {
		return <Title>The file contains unmasked credit card data ({text})</Title>
	}
	if (key === 'sourceCurrencyCode') {
		return (
			<Title>The file does not contain source currency code ({text})</Title>
		)
	}
	if (key === 'incorrectCharacters') {
		return (
			<Title>
				The file contains non-english characters, only the following special
				characters are allowed:`&$(),: ({text})
			</Title>
		)
	}
	if (key === 'incorrectDates') {
		return (
			<Title>
				The file contains an incorrect date format, dates should be DD-MMM-YYYY
				({text})
			</Title>
		)
	}
	if (key === 'stateShouldBeBlank') {
		return <Title>The State value should be blank ({text})</Title>
	}
	if (key === 'stateMissing') {
		return <Title>The State value is missing ({text})</Title>
	}
	if (key === 'stateInvalid') {
		return <Title>Invalid two letter State Code ({text})</Title>
	}
	if (key === 'incorrectTemplate') {
		return <Title>Invalid template format({text})</Title>
	}
	if (key === 'missingRequired') {
		return <Title>Required fields are missing({text})</Title>
	}
	if (key === 'dataType') {
		return <Title>Invalid data type({text})</Title>
	}
	if (key === 'invalidCityName') {
		return <Title>Invalid city name({text})</Title>
	}
	if (key === 'invalidCheckout') {
		return <Title>Invalid Check-Out dates({text})</Title>
	}
	if (key === 'invalidSpend') {
		return <Title>Invalid spend amounts({text})</Title>
	}
	if (key === 'fileExists') {
		return <Title>File has already been ignested({text})</Title>
	}
}

export const getSectionHeader = (key, count) => {
	if (key === 'unmaskedCreditCardData') {
		return <Title key={key}>Unmasked credit card data ({count} errors)</Title>
	}
	if (key === 'sourceCurrencyCode') {
		return <Title key={key}>No source currency code ({count} errors)</Title>
	}
	if (key === 'incorrectCharacters') {
		return (
			<Title key={key}>
				Non-English or unallowed character used ({count} errors)
			</Title>
		)
	}
	if (key === 'incorrectDates') {
		return <Title key={key}>Incorrect date format ({count} errors)</Title>
	}
	if (key === 'stateShouldBeBlank') {
		return (
			<Title key={key}>
				Incorrect State value, State should be blank ({count} errors)
			</Title>
		)
	}
	if (key === 'stateMissing') {
		return (
			<Title key={key}>
				Incorrect State value, State is missing ({count} errors)
			</Title>
		)
	}
	if (key === 'stateInvalid') {
		return (
			<Title key={key}>
				Incorrect State value, State code is invalid ({count} errors)
			</Title>
		)
	}
	if (key === 'incorrectTemplate') {
		return <Title key={key}>Invalid Template Format ({count} errors)</Title>
	}
	if (key === 'missingRequired') {
		return <Title key={key}>Required Fields are Missing ({count} errors)</Title>
	}
	if (key === 'dataType') {
		return <Title key={key}>Invalid Data Types ({count} errors)</Title>
	}
	if (key === 'invalidCityName') {
		return <Title key={key}>Invalid City Name ({count} errors)</Title>
	}
	if (key === 'invalidCheckout') {
		return <Title key={key}>Invalid Check-Out Dates ({count} errors)</Title>
	}
	if (key === 'invalidSpend') {
		return <Title key={key}>Invalid Spend Amounts ({count} errors)</Title>
	}
	if (key === 'fileExists') {
		return (
			<Title key={key}>File has Already Been Ingested ({count} errors)</Title>
		)
	}
}

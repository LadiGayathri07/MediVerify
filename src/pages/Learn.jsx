import React from 'react';
import { Link } from 'react-router-dom';

const Learn = () => {
    return (
        <div className="p-6 max-w-4xl mx-auto bg-white rounded-xl shadow-md space-y-4">
            <h1 className="text-2xl font-bold text-gray-800">Understanding Fake Medical Certificates</h1>
            <p className="text-gray-600">
                Fake medical certificates can be used for fraudulent activities and pose serious legal consequences.
                Here are key indicators to identify fraudulent documents:
            </p>
            <ul className="list-disc list-inside text-gray-700">
                <li>Incorrect or missing hospital/clinic details</li>
                <li>Fake doctor names or unregistered medical IDs</li>
                <li>Suspicious fonts, formatting inconsistencies</li>
                <li>QR codes that do not lead to official verification</li>
                <li>Unrealistic dates (weekends, holidays, past-dated approvals)</li>
            </ul>
            <h2 className="text-xl font-semibold text-gray-800">How Our System Helps</h2>
            <p className="text-gray-600">
                Our AI-driven verification system analyzes document structure, cross-checks databases, and detects anomalies.
                Always ensure you are submitting documents from legitimate sources.
            </p>
            <h2 className="text-xl font-semibold text-gray-800">Additional Resources</h2>
            <ul className="list-disc list-inside text-gray-700">
                <li><a href="https://www.medicalboard.gov.au" className="text-blue-500">Medical Board Verification</a></li>
                <li><a href="https://www.interpol.int/Crimes/Document-Fraud" className="text-blue-500">Interpol - Document Fraud</a></li>
            </ul>
            <div className="text-center mt-6">
                <Link to="/" className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-md hover:bg-blue-700">
                    Back to Home
                </Link>
            </div>
        </div>
    );
};
export default Learn;
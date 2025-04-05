import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
const Header = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState('');

  const handleImageChange = (event) => {
    const files = event.target.files[0];
    if (files) {
      setFile(files);
      setFilename(files.name);
      console.log("File selected:", files);
    }
  };

  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
      // window.location.href = `/result`;
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
       
        const result = await response.json();
        console.log("File uploaded successfully:", result);
        navigate("/result",{state:{result}})
      
      }else{
        const result = await response.json();
        console.log("File uploaded successfully:", result);
        navigate("/result",{state:{result}})
      }
    } catch (error) {
      console.error("Error during upload:", error);
      alert("Error during upload.");
    }
  };

  return (
    <div className="flex flex-col justify-center items-center text-center my-20">
      <div className="text-gray-500 inline-flex items-center gap-2 bg-white px-6 py-1 rounded-full border border-neutral-500">
        <p>🔍 Trusted Verification for Medical Certificates.</p>
        <img src="" alt="" className="h-6" />
      </div>

      <h1 className="text-3xl max-w-[500px] sm:text-7xl sm:max-w-[800px] mx-auto mt-10 text-center leading-tight">
        Detect <span className="text-blue-600">Fake</span> Medical <br />
        Certificates <br /> with
        Secure Verification
      </h1>


      <p className="text-center max-w-xl mx-auto mt-5">
      Ensure your medical certificates are legitimate and fraud-free with our secure verification system. Designed for hospitals, businesses, and individuals who need trustworthy validation.
      </p>

      <form action="" onSubmit={handleUpload} name="upload-form">
      <button
        type="button"
        className="sm:text-lg text-white bg-black w-auto mt-8 px-12 py-2.5 flex items-center gap-2 justify-center rounded-full mx-auto"
        onClick={() => document.getElementById("file-input").click()}
      >
        <input
          id="file-input"
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="hidden"
        />
        Upload Certificate
        <img src="data:image/png;base64,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" alt="" className='h-6 rotate-180' />
      </button>
      {filename && <p className=" text-sm transition-transform">{filename} selected</p>}
      <button
        type="submit"
        className="sm:text-lg text-white bg-black w-auto mt-2 px-12 py-2.5 flex items-center gap-2 justify-center rounded-full mx-auto"
      >
Authenticate    </button>
    </form>
    </div>
  );
};

export default Header;

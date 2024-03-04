import React, { useState } from "react";

const OCRContext = React.createContext({
  activePage: 0,
  originalImage: null,
  actualImage: null,
  textResult: null,
  extractedData: null,
  file: null,
  invoiceId: null,
  isInvoice: true,
  vendorList: [], // Add vendorList to the context
  setActivePage: (activePage) => {},
  setOriginalImage: (image) => {},
  setActualImage: (image) => {},
  setTextResult: (text) => {},
  setExtractedData: (data) => {},
  setFile: (file) => {},
  setInvoiceId: (invoice_id) => {},
  setIsInvoice: (isInvoice) => {},
  setVendorList: (vendorList) => {}, // Add setter for vendorList
});

export const OCRContextProvider = (props) => {
  const [activePage, setActivePage] = useState(0);
  const [originalImage, setOriginalImage] = useState(null);
  const [actualImage, setActualImage] = useState(null);
  const [textResult, setTextResult] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [file, setFile] = useState(null);
  const [invoiceId, setInvoiceId] = useState(null);
  const [isInvoice, setIsInvoice] = useState(true);
  const [vendorList, setVendorList] = useState([]); // Initialize vendorList with an empty array

  const pageHandler = (activePage) => {
    setActivePage(activePage);
  };

  const contextValue = {
    activePage,
    originalImage,
    actualImage,
    textResult,
    extractedData,
    file,
    invoiceId,
    isInvoice,
    vendorList,
    setActivePage: pageHandler,
    setOriginalImage,
    setActualImage,
    setTextResult,
    setExtractedData,
    setFile,
    setInvoiceId,
    setIsInvoice,
    setVendorList, // Add setter for vendorList
  };

  return (
    <OCRContext.Provider value={contextValue}>
      {props.children}
    </OCRContext.Provider>
  );
};

export default OCRContext;

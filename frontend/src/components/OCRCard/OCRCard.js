import React, { useContext, useState } from "react";
import { useSnackbar } from "notistack";
import { Typography, Grid, CircularProgress } from "@mui/material";
import { useStyles } from "./styles";
import ButtonOutlined from "../StyledComponents/ButtonOutlined";
import httpRequest from "../../httpRequest";
import OCRContext from "../../context/ocr-context";

const OCRCard = () => {
  const classes = useStyles();
  const ocrCtx = useContext(OCRContext);
  const [loading, setLoading] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

  const handleOCRmethod = async () => {
    setLoading(true);

    if (ocrCtx.actualImage) {
      const formData = new FormData();
      formData.append("file", ocrCtx.actualImage);

      try {
        const resp = await httpRequest.post(
          "http://localhost:5000/process-invoice-ocr",
          formData
        );

        console.log("Axios Response:", resp);

        if (resp.data.success) {
          ocrCtx.setIsInvoice(true);
          ocrCtx.setTextResult(resp.data.ocr_text);
          ocrCtx.setExtractedData(resp.data.extracted_data); // Update with extracted data
          ocrCtx.setInvoiceId(resp.data.invoice_id);
          ocrCtx.setActivePage(3);
        } else {
          enqueueSnackbar("OCR process was not successful", {
            variant: "error",
          });
        }
      } catch (error) {
        console.error("Error in OCR request", error);
        console.log("Axios Error:", error.response);
        enqueueSnackbar(`Error in OCR request: ${error.message}`, {
          variant: "error",
        });
      }
    } else {
      enqueueSnackbar("Error: No file selected", { variant: "error" });
    }

    setLoading(false);
  };

  return (
    <>
      <div className={classes.rootContainer}>
        <Typography variant="h5" sx={{ pt: 2, fontFamily: "Oxanium, cursive" }}>
          Process Invoice OCR
        </Typography>

        <Grid container spacing={0} sx={{ mt: "15px" }}>
          <Grid item xs={12}>
            <ButtonOutlined
              onClick={handleOCRmethod}
              style={{
                padding: "6px 18px",
              }}
              disabled={loading}
            >
              Process Invoice OCR
            </ButtonOutlined>
          </Grid>
        </Grid>

        {loading && <CircularProgress sx={{ color: "#854de0", mt: "15px" }} />}
      </div>
    </>
  );
};

export default OCRCard;

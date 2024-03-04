import React, { useState, useEffect } from "react";
import { Paper, TextField, Grid } from "@mui/material";
import { useStyles } from "./styles";

const InvoiceTable = (props) => {
  const classes = useStyles();
  const invoiceData = props.data || {};
  const [localData, setLocalData] = useState(invoiceData);

  useEffect(() => {
    setLocalData(invoiceData);
  }, [invoiceData]);

  const handleChange = (event, field) => {
    const newData = { ...localData, [field]: event.target.value };
    setLocalData(newData);
    props.onDataChange(newData);
  };

  const renderTextField = (field, label, index) => (
    <Grid item xs={6} key={index}>
      <TextField
        label={label}
        value={localData[field] || ""}
        onChange={(event) => handleChange(event, field)}
        variant="standard"
        className={classes.focused}
        fullWidth
        inputProps={{ style: { fontWeight: "bold" } }}
      />
    </Grid>
  );

  // Define fields to display in the table
  const fields = [
    { field: "vendor_name", label: "Vendor name" },
    { field: "invoice_number", label: "Invoice number" },
    { field: "invoice_date", label: "Invoice date" },
    { field: "invoice_amount", label: "Invoice amount" },
  ];

  return (
    <div className={classes.table}>
      <Paper elevation={3} sx={{ p: 2, borderRadius: 5 }}>
        <Grid container spacing={1}>
          {fields.map((field, index) =>
            renderTextField(field.field, field.label, index)
          )}
        </Grid>
      </Paper>
    </div>
  );
};

export default InvoiceTable;

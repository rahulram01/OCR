import { useState, useEffect } from "react";
import { Paper, TextField, ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#854de0",
    },
  },
});

function DataTable(props) {
  const { data, ico } = props;
  const [localData, setLocalData] = useState(data);

  useEffect(() => {
    const newData = { ...data, ICO: ico !== undefined ? ico : data?.ICO };
    setLocalData(newData);
  }, [data, ico]);

  const handleChange = (event, field) => {
    const newData = { ...localData, [field]: event.target.value };
    setLocalData(newData);
    props.onDataChange(newData);
  };
  const renderTextField = (field, label) => (
    <TextField
      label={label}
      value={localData && localData[field] ? localData[field] : ""}
      onChange={(event) => handleChange(event, field)}
      sx={{ mb: 1 }}
      variant="standard"
      fullWidth
      inputProps={{ style: { fontWeight: "bold" } }}
    />
  );

  return <ThemeProvider theme={theme}></ThemeProvider>;
}

export default DataTable;

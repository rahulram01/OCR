import { makeStyles } from "@mui/styles";

export const useStyles = makeStyles({
  rootContainer: {
    position: "relative",
    color: "white",
    backgroundColor: "#040053",
    textAlign: "center",
    width: "250px",
    transition: "width 0.3s ease-in-out",
  },
  logo: {
    transition: "transform 0.3s ease-in-out",
    height: "100px;",
  },

  // Apply the zoom effect on hover
  logoZoomed: {
    transform: "scale(2.0)", // Adjust the scale factor as needed
  },

  rootContainerCollapsed: {
    width: "0",
  },
  closeContainer: {
    textAlign: "right",
  },
  linkContainer: {
    marginTop: 10,
  },
  closeButton: {
    textAlign: "right",
    color: "white",
  },
  footerContainer: {
    marginBottom: 20,
    display: "none",
  },

  "@media (max-width:590px)": {
    footerContainer: {
      display: "block",
    },
  },
});

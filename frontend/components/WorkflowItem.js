import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Chip,
  Stepper,
  Step,
  StepLabel,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

// Define workflow statuses and corresponding colors
const statusSteps = [
  { label: "Generating Runs", color: "#ff9800" }, // Orange
  { label: "Launching to Queue", color: "#ffca28" }, // Amber
  { label: "Waiting for Jobs", color: "#fdd835" }, // Yellow
  { label: "Writing Forcefield", color: "#8bc34a" }, // Light Green
  { label: "Ready for Download", color: "#4caf50" }, // Green
];

// Function to get step index from status
const getStepIndex = (status) => {
  const stepIndex = statusSteps.findIndex(
    (step) => step.label.toLowerCase() === status.toLowerCase()
  );
  return stepIndex !== -1 ? stepIndex : 0; // Default to first step if status is unknown
};

export default function WorkflowItem({ workflow }) {
  const activeStep = getStepIndex(workflow.status);
  const workflowIdTag = `ID: ${workflow._id.slice(-6)}`; 

  return (
    <Accordion
      sx={{ width: "100%", marginBottom: "10px", fontFamily: "system-ui" }}
    >
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography
          variant="h6"
          sx={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            width: "100%",
            justifyContent: "space-between",
          }}
        >
          {/* Left Section: Prefix + Status */}
          <span style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            {workflow.prefix}
            <Chip
              label={statusSteps[activeStep].label}
              sx={{
                backgroundColor: statusSteps[activeStep].color,
                color: "#fff",
                fontWeight: "bold",
              }}
            />
          </span>

          {/* Right Section:  ID + Expand Icon */}
          <span
            style={{
              display: "flex",
              alignItems: "center",
              marginRight: "10px",
            }}
          >
            <Chip
              label={workflowIdTag}
              sx={{ backgroundColor: "#e0e0e0", color: "#333" }}
            />
          </span>
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Typography>
          <strong>Purpose:</strong> {workflow.purpose}
        </Typography>
        <Typography>
          <strong>Trained on:</strong> {workflow.max_structures} structures
        </Typography>
        <Typography>
          <strong>Submitted at:</strong>{" "}
          {new Intl.DateTimeFormat("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
            hour12: true,
          }).format(new Date(workflow.created_at))}
        </Typography>

        {/* Progress Stepper*/}
        <Typography sx={{marginBottom: "10px"}}>
          <strong>Current Action:</strong>
        </Typography>
        <span
          style={{marginTop: "10px", marginBottom: "10px"}}
        >
          <Stepper activeStep={activeStep} alternativeLabel>
            {statusSteps.map((step, index) => (
              <Step key={step.label}>
                <StepLabel
                  sx={{ color: activeStep >= index ? step.color : "#bdbdbd" }}
                >
                  {step.label}
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        </span>
      </AccordionDetails>
    </Accordion>
  );
}

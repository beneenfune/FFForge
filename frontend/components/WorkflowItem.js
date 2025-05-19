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
import { useState } from "react";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

// Map backend statuses to UI labels and colors
const statusMap = {
  "generating runs": { label: "Generating Jobs", color: "#ff9800" },
  "launching to queue": { label: "Submitting Jobs", color: "#ffca28" },
  "waiting for jobs": { label: "Waiting for Jobs", color: "#fdd835" },
  writing: { label: "Writing Forcefield", color: "#8bc34a" },
  complete: { label: "Ready to Download", color: "#4caf50" },
};

// Define the correct step order for the stepper
const orderedStatuses = [
  "generating runs",
  "launching to queue",
  "waiting for jobs",
  "writing",
  "complete",
];

// Get step index from status string
const getStepIndex = (status) => {
  const normalized = status.toLowerCase();
  const index = orderedStatuses.indexOf(normalized);
  return index !== -1 ? index : 0;
};

export default function WorkflowItem({ workflow }) {
  const normalizedStatus = workflow.status.toLowerCase();
  const activeStep = getStepIndex(normalizedStatus);
  const currentStatus = statusMap[normalizedStatus] || {
    label: workflow.status,
    color: "#9e9e9e",
  };
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);

  const workflowIdTag = `ID: ${workflow._id.slice(-6)}`;

  return (
    <>
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
              label={currentStatus.label}
              sx={{
                backgroundColor: currentStatus.color,
                color: "#fff",
                fontWeight: "bold",
              }}
            />
          </span>

          {/* Right Section: ID */}
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
        <div 
        style ={{ 
          display: "flex", 
          justifyContent: "space-between", 
          gap: "20px"
          }}
        >
          {/* Left Section: Info */}
          <div style = {{flex: 1}}>
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
          </div>

          {/* Right Section: Image */}
          <div 
            style = {{
              flexShrink: 0, 
              width: "20%", 
              minWidth: "120px", 
              display: "flex", 
              justifyContent: "flex-end"
            }}
            onClick={() => setIsLightboxOpen(true)}
          >
            <img
            src="/images/mlff_plot_placeholder.png"
            alt="MLFF accuracy plot"
            style={{
              width: "100%",
              height:"auto",
              }}
            />
          </div>
        </div>

        {/* Progress Stepper */}
        <Typography sx={{ marginBottom: "10px" }}>
          <strong>Current Action:</strong>
        </Typography>
        <span style={{ marginTop: "10px", marginBottom: "10px" }}>
          <Stepper activeStep={activeStep} alternativeLabel>
            {orderedStatuses.map((key, index) => (
              <Step key={key}>
                <StepLabel
                  sx={{
                    color:
                      activeStep >= index ? statusMap[key].color : "#bdbdbd",
                  }}
                >
                  {statusMap[key].label}
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        </span>
      </AccordionDetails>
    </Accordion>
    {/* Lightbox */}
    {isLightboxOpen && (
      <div
        onClick={() => setIsLightboxOpen(false)}
        style= {{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
          backgroundColor: "rgba(0,0,0,0.8)",
          display:"flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 9999,
        }}
      >
        <img
        src="/images/mlff_plot_placeholder.png"
        alt="MLFF accuracy plot"
        style={{
          maxWidth: "100%",
          maxHeight: "100%",
          boxShadow: "0 0 20px rgba(0,0,0,0.5)",
          backgroundColor: "white",
          padding: "10px",
          }}
        />
      </div>
    )}
  </>
  );
}

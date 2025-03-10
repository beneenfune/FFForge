"use client";

import { useEffect, useState } from "react";
import styles from "../../styles/Landing.module.css";
import Layout from "../../components/Layout";
import WorkflowItem from "../../components/WorkflowItem";
import { CircularProgress, Typography } from "@mui/material";

export default function MyWorkflows() {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWorkflows = async () => {
      try {
        const response = await fetch("/api/v1/workflow/all");
        const data = await response.json();
        setWorkflows(data.workflows); // Ensure accessing `data.workflows`
      } catch (error) {
        console.error("Error fetching workflows:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchWorkflows();
  }, []);

  return (
    <Layout>
      <div className={styles.body}>
        <div className={styles.content}>
          <h3 className={styles.heading3}>My MLFF Workflows</h3>

          {loading ? (
            <CircularProgress />
          ) : workflows.length === 0 ? (
            <Typography>No workflows found.</Typography>
          ) : (
            workflows.map((workflow) => (
              <WorkflowItem key={workflow._id} workflow={workflow} />
            ))
          )}
        </div>
      </div>
    </Layout>
  );
}

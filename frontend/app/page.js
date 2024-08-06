'use client';

import { useState, useEffect } from 'react'
import styles from "./page.module.css";

export default function Home() {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_BASE_URL + '/api/')
        .then(res => {
            if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            setMessage(data.homepage);
            setLoading(false);
        })
        .catch(err => {
            setError(err.message);
            setLoading(false);
        });
    }, []);

    return (
        <div className={styles.container}>
          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p>Error: {error}</p>
          ) : (
            <p>{message}</p>
          )}
        </div>
      );
    }
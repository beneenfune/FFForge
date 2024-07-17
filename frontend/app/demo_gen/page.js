'use client';

import { useEffect, useState } from 'react'
import styles from "./page.module.css";

export default function Home() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  fetch('http://127.0.0.1:8000/api/demo_gen')
      .then(res => res.json())
      .then(data => {
          setMessage(data.demo_gen);
          setLoading(false);
      })

    return (
        <div className={styles.container}>
            <p> {!loading ? message : "Loading.."}</p>
        </div>
    );
}
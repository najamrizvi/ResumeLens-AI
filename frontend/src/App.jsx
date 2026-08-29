import { useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

const ALLOWED_EXTENSIONS = [".pdf", ".docx"];

const ALLOWED_MIME_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

function App() {
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const [uploadedFile, setUploadedFile] = useState(null);

  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // ============================================================
  // RESUME UPLOAD
  // ============================================================

  const uploadResume = async (file) => {
    setError("");
    setResult(null);

    if (!file) {
      return;
    }

    const fileName = file.name.toLowerCase();

    const hasValidExtension = ALLOWED_EXTENSIONS.some(
      (extension) => fileName.endsWith(extension)
    );

    const hasValidMimeType = ALLOWED_MIME_TYPES.includes(file.type);

    if (!hasValidExtension && !hasValidMimeType) {
      setError(
        "Unsupported file type. Please upload a PDF or DOCX resume."
      );
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError(
        "File is too large. Maximum allowed size is 5 MB."
      );
      return;
    }

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/api/upload-resume`,
        {
          method: "POST",
          body: formData,
        }
      );

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            `Resume upload failed with status ${response.status}.`
        );
      }

      if (
        !data ||
        typeof data.resume_text !== "string" ||
        !data.resume_text.trim()
      ) {
        throw new Error(
          "The backend did not return readable resume content."
        );
      }

      setResumeText(data.resume_text);

      setUploadedFile({
        name: data.filename || file.name,
        type:
          data.file_type ||
          (fileName.endsWith(".pdf") ? "PDF" : "DOCX"),
        size: Number.isFinite(Number(data.file_size))
          ? Number(data.file_size)
          : file.size,
        characters: Number.isFinite(Number(data.character_count))
          ? Number(data.character_count)
          : data.resume_text.length,
      });
    } catch (err) {
      setUploadedFile(null);
      setResumeText("");

      setError(
        err?.message ||
          "Unable to upload the resume. Please make sure the backend is running."
      );
    } finally {
      setUploading(false);
    }
  };

  // ============================================================
  // FILE INPUT
  // ============================================================

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (file) {
      uploadResume(file);
    }

    event.target.value = "";
  };

  // ============================================================
  // DRAG & DROP
  // ============================================================

  const handleDrop = (event) => {
    event.preventDefault();

    if (uploading || loading) {
      return;
    }

    const file = event.dataTransfer.files?.[0];

    if (file) {
      uploadResume(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  // ============================================================
  // ANALYZE RESUME
  // ============================================================

  const analyzeResume = async () => {
    setError("");
    setResult(null);

    if (resumeText.trim().length < 20) {
      setError(
        "Please upload a valid resume with readable content before analyzing."
      );
      return;
    }

    if (jobDescription.trim().length < 20) {
      setError(
        "Please enter a job description with at least 20 characters."
      );
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        `${API_URL}/api/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            resume_text: resumeText.trim(),
            job_description: jobDescription.trim(),
          }),
        }
      );

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            `Resume analysis failed with status ${response.status}.`
        );
      }

      if (!data || typeof data !== "object") {
        throw new Error(
          "The backend returned an invalid analysis response."
        );
      }

      const normalizedResult = {
        predicted_category: String(
          data.predicted_category || "Unknown"
        ),

        fit_score: Number.isFinite(Number(data.fit_score))
          ? Number(data.fit_score)
          : 0,

        resume_skills: Array.isArray(data.resume_skills)
          ? data.resume_skills
          : [],

        required_skills: Array.isArray(data.required_skills)
          ? data.required_skills
          : [],

        matched_skills: Array.isArray(data.matched_skills)
          ? data.matched_skills
          : [],

        missing_skills: Array.isArray(data.missing_skills)
          ? data.missing_skills
          : [],

        total_required_skills: Number.isFinite(
          Number(data.total_required_skills)
        )
          ? Number(data.total_required_skills)
          : 0,
      };

      normalizedResult.fit_score = Math.min(
        100,
        Math.max(0, normalizedResult.fit_score)
      );

      setResult(normalizedResult);
    } catch (err) {
      setError(
        err?.message ||
          "Unable to connect to the ResumeLens AI backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // CLEAR
  // ============================================================

  const clearAnalysis = () => {
    setResumeText("");
    setJobDescription("");
    setUploadedFile(null);
    setResult(null);
    setError("");
  };

  // ============================================================
  // FORMAT FILE SIZE
  // ============================================================

  const formatFileSize = (bytes) => {
    if (!Number.isFinite(Number(bytes)) || Number(bytes) <= 0) {
      return "0 KB";
    }

    return `${(Number(bytes) / 1024).toFixed(1)} KB`;
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="app-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      {/* NAVIGATION */}

      <header className="navbar">
        <div className="brand">
          <div className="brand-mark">
            <span />
            <span />
            <span />
          </div>

          <div>
            <div className="brand-name">
              ResumeLens
            </div>

            <div className="brand-subtitle">
              AI Career Intelligence
            </div>
          </div>
        </div>

        <div className="nav-status">
          <span className="status-dot" />
          AI Engine Ready
        </div>
      </header>

      <main className="main-content">
        {/* HERO */}

        <section className="hero">
          <div className="eyebrow">
            <span className="eyebrow-dot" />
            Intelligent Resume Analysis
          </div>

          <h1>
            Understand your resume.
            <br />
            <span>
              Discover your career fit.
            </span>
          </h1>

          <p className="hero-description">
            ResumeLens AI analyzes your resume against a
            target job, identifies relevant skills, detects
            missing requirements, and predicts your career
            category.
          </p>
        </section>

        {/* WORKSPACE */}

        <section className="workspace">
          <div className="workspace-header">
            <div>
              <span className="section-kicker">
                ANALYSIS WORKSPACE
              </span>

              <h2>
                Compare your experience with the opportunity.
              </h2>
            </div>

            {(resumeText ||
              jobDescription ||
              result ||
              uploadedFile) && (
              <button
                type="button"
                className="clear-button"
                onClick={clearAnalysis}
                disabled={uploading || loading}
              >
                Clear
              </button>
            )}
          </div>

          {/* INPUT GRID */}

          <div className="input-grid">
            {/* RESUME UPLOAD */}

            <div className="glass-panel input-panel">
              <div className="panel-heading">
                <div className="panel-icon resume-icon">
                  R
                </div>

                <div>
                  <h3>
                    Your Resume
                  </h3>

                  <p>
                    Upload your PDF or DOCX resume
                  </p>
                </div>
              </div>

              {!uploadedFile ? (
                <label
                  className={`upload-zone ${
                    uploading ? "uploading" : ""
                  }`}
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                >
                  <input
                    type="file"
                    accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    onChange={handleFileChange}
                    disabled={uploading || loading}
                  />

                  <div className="upload-icon">
                    {uploading ? "…" : "↑"}
                  </div>

                  <strong>
                    {uploading
                      ? "Processing resume..."
                      : "Upload your resume"}
                  </strong>

                  <span>
                    {uploading
                      ? "Extracting resume content"
                      : "Drag & drop or click to browse"}
                  </span>

                  <small>
                    PDF or DOCX · Maximum 5 MB
                  </small>
                </label>
              ) : (
                <div className="uploaded-resume">
                  <div className="uploaded-file-icon">
                    {uploadedFile.type === "PDF"
                      ? "PDF"
                      : "DOC"}
                  </div>

                  <div className="uploaded-file-info">
                    <strong>
                      {uploadedFile.name}
                    </strong>

                    <span>
                      {uploadedFile.type} ·{" "}
                      {formatFileSize(uploadedFile.size)}
                    </span>
                  </div>

                  <div className="upload-success">
                    ✓
                  </div>
                </div>
              )}

              {uploadedFile && (
                <div className="upload-meta">
                  <span>
                    ✓ Resume text extracted
                  </span>

                  <span>
                    {Number(
                      uploadedFile.characters || 0
                    ).toLocaleString()}{" "}
                    characters
                  </span>
                </div>
              )}

              {uploadedFile && (
                <div className="resume-preview">
                  <span className="preview-label">
                    EXTRACTED CONTENT
                  </span>

                  <p>
                    {resumeText.slice(0, 280)}
                    {resumeText.length > 280
                      ? "..."
                      : ""}
                  </p>
                </div>
              )}
            </div>

            {/* JOB DESCRIPTION */}

            <div className="glass-panel input-panel">
              <div className="panel-heading">
                <div className="panel-icon job-icon">
                  J
                </div>

                <div>
                  <h3>
                    Target Job
                  </h3>

                  <p>
                    Paste the job description
                  </p>
                </div>
              </div>

              <textarea
                value={jobDescription}
                onChange={(event) => {
                  setJobDescription(event.target.value);

                  if (error) {
                    setError("");
                  }
                }}
                disabled={uploading || loading}
                placeholder={`Paste the target job description here...

Example:
We need a Machine Learning Engineer with Python, TensorFlow, Docker, SQL, scikit-learn and data analysis experience.`}
              />

              <div className="textarea-footer">
                <span>
                  {jobDescription.length} characters
                </span>

                <span className="input-hint">
                  Job requirements
                </span>
              </div>
            </div>
          </div>

          {/* ANALYSIS ACTION */}

          <div className="analysis-action">
            <button
              type="button"
              className={`analyze-button ${
                loading ? "loading" : ""
              }`}
              onClick={analyzeResume}
              disabled={loading || uploading}
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  Analyzing your profile...
                </>
              ) : (
                <>
                  <span className="button-spark">
                    ✦
                  </span>

                  Analyze Resume

                  <span className="button-arrow">
                    →
                  </span>
                </>
              )}
            </button>

            <p>
              Powered by ResumeLens AI intelligence engine
            </p>
          </div>

          {/* ERROR */}

          {error && (
            <div
              className="error-message"
              role="alert"
            >
              <span>
                !
              </span>

              {error}
            </div>
          )}
        </section>

        {/* RESULTS */}

        {result && (
          <section className="results-section">
            <div className="results-header">
              <div>
                <span className="section-kicker">
                  ANALYSIS COMPLETE
                </span>

                <h2>
                  Your Resume Intelligence Report
                </h2>
              </div>

              <div className="analysis-badge">
                <span className="status-dot" />
                Analysis complete
              </div>
            </div>

            {/* TOP METRICS */}

            <div className="metrics-grid">
              <div className="result-card fit-card">
                <div className="card-label">
                  JOB FIT SCORE
                </div>

                <div className="score-display">
                  <div
                    className="score-ring"
                    style={{
                      "--score": Math.round(
                        result.fit_score
                      ),
                    }}
                  >
                    <div>
                      <strong>
                        {Math.round(result.fit_score)}
                      </strong>

                      <span>
                        %
                      </span>
                    </div>
                  </div>

                  <div>
                    <h3>
                      {result.fit_score >= 80
                        ? "Strong Match"
                        : result.fit_score >= 60
                        ? "Good Potential"
                        : "Needs Improvement"}
                    </h3>

                    <p>
                      Based on required skill alignment
                    </p>
                  </div>
                </div>
              </div>

              <div className="result-card category-card">
                <div className="card-label">
                  PREDICTED CAREER CATEGORY
                </div>

                <div className="category-content">
                  <div className="category-symbol">
                    ✦
                  </div>

                  <div>
                    <h3>
                      {result.predicted_category}
                    </h3>

                    <p>
                      ML-powered career classification
                    </p>
                  </div>
                </div>
              </div>

              <div className="result-card required-card">
                <div className="card-label">
                  REQUIRED SKILLS
                </div>

                <div className="large-number">
                  {result.total_required_skills}
                </div>

                <p>
                  skills identified in the job description
                </p>
              </div>
            </div>

            {/* SKILL COMPARISON */}

            <div className="skill-grid">
              <div className="result-card skill-card">
                <div className="skill-card-header">
                  <div>
                    <span className="card-label">
                      MATCHED SKILLS
                    </span>

                    <h3>
                      What you already have
                    </h3>
                  </div>

                  <span className="skill-count matched-count">
                    {result.matched_skills.length}
                  </span>
                </div>

                <div className="skill-list">
                  {result.matched_skills.length > 0 ? (
                    result.matched_skills.map(
                      (skill, index) => (
                        <span
                          className="skill-pill matched"
                          key={`${skill}-${index}`}
                        >
                          <span>
                            ✓
                          </span>

                          {skill}
                        </span>
                      )
                    )
                  ) : (
                    <p className="empty-state">
                      No matching skills detected.
                    </p>
                  )}
                </div>
              </div>

              <div className="result-card skill-card">
                <div className="skill-card-header">
                  <div>
                    <span className="card-label">
                      MISSING SKILLS
                    </span>

                    <h3>
                      Areas to strengthen
                    </h3>
                  </div>

                  <span className="skill-count missing-count">
                    {result.missing_skills.length}
                  </span>
                </div>

                <div className="skill-list">
                  {result.missing_skills.length > 0 ? (
                    result.missing_skills.map(
                      (skill, index) => (
                        <span
                          className="skill-pill missing"
                          key={`${skill}-${index}`}
                        >
                          <span>
                            +
                          </span>

                          {skill}
                        </span>
                      )
                    )
                  ) : (
                    <p className="empty-state">
                      Excellent. No missing required
                      skills detected.
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* COMPLETE REQUIREMENTS */}

            <div className="result-card all-skills-card">
              <div className="skill-card-header">
                <div>
                  <span className="card-label">
                    JOB REQUIREMENTS
                  </span>

                  <h3>
                    Complete required skill profile
                  </h3>
                </div>
              </div>

              <div className="skill-list">
                {result.required_skills.length > 0 ? (
                  result.required_skills.map(
                    (skill, index) => {
                      const matched =
                        result.matched_skills.includes(
                          skill
                        );

                      return (
                        <span
                          className={`skill-pill ${
                            matched
                              ? "matched"
                              : "missing"
                          }`}
                          key={`${skill}-${index}`}
                        >
                          <span>
                            {matched ? "✓" : "+"}
                          </span>

                          {skill}
                        </span>
                      );
                    }
                  )
                ) : (
                  <p className="empty-state">
                    No specific skills were identified
                    in the job description.
                  </p>
                )}
              </div>
            </div>
          </section>
        )}

        {/* FOOTER */}

        <footer className="footer">
          <div>
            <strong>
              ResumeLens AI
            </strong>

            <span>
              Intelligent career analysis powered by
              machine learning.
            </span>
          </div>

          <span className="footer-version">
            v1.0
          </span>
        </footer>
      </main>
    </div>
  );
}

export default App;
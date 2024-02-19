[![Pipeline API flask](https://github.com/w0Iff/api_pipeline/actions/workflows/pipeline.yml/badge.svg?branch=main)](https://github.com/w0Iff/api_pipeline/actions/workflows/pipeline.yml)

CI/CD Pipeline for Flask Api 

Build ───▶

           │
           └───► 3 x Unit Tests 

"SAST" ───▶

           │
           └───►- CodeQL Analysis (Python)

"SCA" ───▶

          │
          └───► Dependency Check
 
"DAST" ───▶

           │
           └───► Hawk Scan




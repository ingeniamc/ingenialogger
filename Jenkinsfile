
/*
 * ingenialogger
 *
 * Copyright (c) 2020 Ingenia Motion Control.
 */

def SW_NODE = "windows-slave"

pipeline {
    agent none
    stages {
        stage('Build wheels and documentation') {
            agent {
                docker {
                    label SW_NODE
                    image 'ingeniacontainers.azurecr.io/win-python-builder:1.0'
                }
            }
            stages {
                stage('Clone repository') {
                    steps {
                        bat """
                            cd C:\\Users\\ContainerAdministrator
                            git clone https://github.com/ingeniamc/ingenialogger.git
                            cd ingenialogger
                            git checkout ${env.GIT_COMMIT}
                        """
                    }
                 }
                stage('Install deps') {
                    steps {
                        bat '''
                            cd C:\\Users\\ContainerAdministrator\\ingenialogger
                            python -m venv venv
                            venv\\Scripts\\python.exe -m pip install -r requirements\\dev-requirements.txt
                            venv\\Scripts\\python.exe -m pip install -e .
                        '''
                    }
                }
                stage('Check formatting') {
                    steps {
                        bat """
                            cd C:\\Users\\ContainerAdministrator\\ingenialogger
                            venv\\Scripts\\python.exe -m black -l 100 --check ingeniamotion tests
                        """
                    }
                }
                stage('Run unit tests') {
                    steps {
                        bat """
                            cd C:\\Users\\ContainerAdministrator\\ingenialogger
                            python -m pipenv run pytest tests --junitxml=pytest_report.xml
                            python -m pipenv run coverage xml --include=ingenialogger/*
                            COPY pytest_report.xml ${env.WORKSPACE}\\pytest_report.xml
                            COPY coverage.xml ${env.WORKSPACE}\\coverage.xml
                        """
                        junit 'pytest_report.xml'
                        publishCoverage adapters: [coberturaReportAdapter('coverage.xml')]
                    }
                }
                stage('Generate documentation') {
                    steps {
                        bat '''
                            cd C:\\Users\\ContainerAdministrator\\ingenialogger
                            venv\\Scripts\\python.exe -m sphinx -b html docs _docs
                        '''
                    }
                }
                stage('Build wheels') {
                    steps {
                        bat '''
                             cd C:\\Users\\ContainerAdministrator\\ingenialogger
                             venv\\Scripts\\python.exe setup.py bdist_wheel
                        '''
                    }
                }
                stage('Archive') {
                    steps {
                        bat """
                            cd C:\\Users\\ContainerAdministrator\\ingenialogger
                            "C:\\Program Files\\7-Zip\\7z.exe" a -r docs.zip -w _docs -mem=AES256
                            XCOPY dist ${env.WORKSPACE}\\dist /i
                            XCOPY docs.zip ${env.WORKSPACE}
                        """
                        archiveArtifacts artifacts: "dist\\*, docs.zip"
                    }
                }
            }
        }
    }
}

# Postman API Automation Project

A comprehensive API testing project built using **Postman, JavaScript, and Postman CLI**, with automated CI execution through **GitHub Actions** and consolidated HTML test reporting.

The project focuses on validating API functionality, response structures, authentication, integration workflows, negative scenarios, and regression behavior.

## Project Highlights

| Metric                     |    Result |
| -------------------------- | --------: |
| Postman collections        |         6 |
| Reported test cases        |       385 |
| Passed test cases          |       385 |
| Failed test cases          |         0 |
| Overall pass rate          |      100% |
| Collections executed in CI |         6 |
| Consolidated HTML report   | Available |

## Technology Stack

- **API Testing:** Postman
- **Scripting:** JavaScript (Postman scripts)
- **CLI Execution:** Postman CLI
- **CI/CD:** GitHub Actions
- **Test Reporting:** JUnit XML and HTML
- **Version Control:** Git and GitHub
- **API Services:** DummyJSON, Frankfurter API, Postman Echo

## Project Structure

```text
postman-api-testing/
│
├── .github/
│   └── workflows/
│       └── postman-api-tests.yml
│
├── collections/
│   ├── Authentication.postman_collection.json
│   ├── Cart_Management.postman_collection.json
│   ├── Integration_Testing.postman_collection.json
│   ├── Product_Management.postman_collection.json
│   ├── Regression_Suite.postman_collection.json
│   └── User_Management.postman_collection.json
│
├── environments/
│   └── qa-public-environment.example.json
│
├── reports/
│
├── .gitignore
└── README.md
```

The actual local environment file is excluded from Git to avoid committing private configuration.

## Postman Collection Coverage

### 1. Authentication Testing

- Login API validation
- Valid and invalid authentication scenarios
- Access token validation
- Refresh token validation
- Response status and structure validation

### 2. Cart Management

- Retrieve all carts
- Retrieve cart by ID
- Create cart
- Update cart
- Delete cart
- Cart structure and data validation

### 3. Integration Testing

- Authentication and user workflow
- Authenticated user profile validation
- User cart integration
- Product and cart integration
- Currency exchange API integration

### 4. Product Management

- Retrieve products
- Search products
- Product details validation
- Category validation
- Sorting and filtering
- Create, update, and delete product scenarios

### 5. Regression Suite

- Authentication regression
- Cart regression
- Product regression
- User regression
- Positive and negative scenario validation

### 6. User Management

- User authentication
- Retrieve users
- Retrieve user by ID
- User search
- User profile validation
- Response and data validation

## API Services Used

| API          | Purpose                                                            |
| ------------ | ------------------------------------------------------------------ |
| DummyJSON    | Mock e-commerce APIs for products, users, carts and authentication |
| Frankfurter  | Currency exchange reference rates                                  |
| Postman Echo | HTTP request and response testing                                  |

**Important:** DummyJSON simulates certain write operations. POST, PUT and DELETE operations should not be interpreted as persistent database changes. Frankfurter provides reference exchange rates, not banking or payment processing.

## Automated CI/CD Pipeline

GitHub Actions automatically executes the six Postman collections.

### Workflow triggers

- Push to `main`
- Pull requests targeting `main`
- Manual execution through GitHub Actions

### Pipeline execution

1. Checkout the GitHub repository.
2. Create the reports directory.
3. Execute the six Postman collections independently.
4. Generate individual JUnit XML reports.
5. Generate individual HTML reports.
6. Combine JUnit results into one consolidated HTML report.
7. Upload the reports as a GitHub Actions artifact.
8. Evaluate the collection execution outcomes.

### Reporting

The pipeline produces:

- Individual collection HTML reports
- Individual JUnit XML reports
- Consolidated HTML dashboard

The consolidated dashboard includes:

- Total test cases
- Passed and failed test cases
- Error and skipped counts
- Overall pass rate
- Collection-wise summary
- Individual test case results

Reports are uploaded as the `API-Quality-Hub-Reports` artifact and retained for 14 days.

## Latest Test Execution Results

| Collection          |   Total |  Passed | Failed |
| ------------------- | ------: | ------: | -----: |
| Authentication      |      30 |      30 |      0 |
| Cart Management     |      33 |      33 |      0 |
| Integration Testing |      31 |      31 |      0 |
| Product Management  |      83 |      83 |      0 |
| Regression Suite    |     175 |     175 |      0 |
| User Management     |      33 |      33 |      0 |
| **Total**           | **385** | **385** |  **0** |

**Overall reported pass rate: 100%**

## How to Run the Project

### Prerequisites

- Postman
- Postman CLI
- Git
- GitHub account

### Step 1: Clone the repository

```bash
git clone https://github.com/K-SAI-GANESH/postman-api-testing.git
```

### Step 2: Navigate to the project

```bash
cd postman-api-testing
```

### Step 3: Configure the environment

Import the example environment into Postman and configure the required variables.

Do not commit private credentials or local environment files.

### Step 4: Execute a collection

Example:

```bash
postman collection run collections/Authentication.postman_collection.json --environment environments/qa-public-environment.example.json
```

Repeat for the other collections as required.

### Step 5: Execute through GitHub Actions

Push changes to the `main` branch or manually trigger the workflow from the repository's Actions tab.

## Skills Demonstrated

- REST API Testing
- Manual API Validation
- API Automation Using Postman
- JavaScript Test Scripting
- Positive and Negative Testing
- Authentication Testing
- Integration Testing
- Regression Testing
- JSON Response Validation
- Environment Variable Management
- Postman CLI
- Git and GitHub
- GitHub Actions CI/CD
- JUnit and HTML Reporting

## Project Scope and Limitations

- The project uses public mock and reference APIs.
- Some write operations are simulated rather than persisted.
- The reported 100% pass rate reflects the recorded test cases in the latest consolidated report, not production API certification.
- Security testing is planned separately and is not included in the current completion claim.
- Performance testing is excluded from the project scope.

## Author

**K Sai Ganesh**

QA Engineer | Manual & Automation Testing

GitHub: https://github.com/K-SAI-GANESH

LinkedIn: https://linkedin.com/in/k-ganesh

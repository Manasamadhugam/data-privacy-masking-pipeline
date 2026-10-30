\# Data Dictionary



\## Project: Data Privacy \& Masking Pipeline



\### 1. Customers Dataset



| Column | Data Type | Description |

|---|---|---|

| customer\_id | String | Unique customer identifier |

| full\_name | String | Customer full name |

| email | String | Customer email address |

| phone | String | Customer phone number |

| date\_of\_birth | Date | Customer date of birth |

| city | String | Customer city |



\### 2. Orders Dataset



| Column | Data Type | Description |

|---|---|---|

| order\_id | String | Unique order identifier |

| customer\_id | String | Customer reference ID |

| order\_date | Date | Date of the order |

| order\_amount | Float | Total order amount |



\### 3. Analytics Output Dataset



| Column | Data Type | Description |

|---|---|---|

| customer\_id | String | Customer identifier |

| full\_name | String | Masked customer name |

| email | String | Masked email address |

| phone | String | Masked phone number |

| city | String | Customer city |

| order\_count | Integer | Total number of orders |

| total\_spend | Float | Total amount spent |

| last\_order\_date | Date | Most recent order date |



\### 4. Rejected Records Dataset



| Column | Data Type | Description |

|---|---|---|

| record\_id | String | ID of rejected record |

| reason | String | Reason for rejection |



\### 5. Privacy Information



\- Customer names are masked.

\- Email usernames are masked.

\- Phone numbers are partially masked.

\- Date of birth is excluded from the analytics output.

\- Only synthetic data is used in this project.


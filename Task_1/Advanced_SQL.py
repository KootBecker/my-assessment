"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

NOTE:
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""


def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    qry =   """
                -- Find the AverageIncome per CustomerClass
                SELECT cr.CustomerClass,
                        ROUND(AVG(cu.Income), 2) AS AverageIncome
                -- Join the customers and credit tables on CustomerID
                FROM customers cu
                JOIN credit cr
                ON cu.CustomerID = cr.CustomerID
                -- Group by CustomerClass
                GROUP BY cr.CustomerClass
            """

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    qry =   """
                -- Find the number of RejectedApplications per Region
                SELECT CASE
                            WHEN c.Region IN ('EasternCape', 'EC') THEN 'EasternCape'
                            WHEN c.Region IN ('FreeState', 'FS') THEN 'FreeState'
                            WHEN c.Region IN ('WesternCape', 'WC') THEN 'WesternCape'
                            WHEN c.Region IN ('NorthWest', 'NW') THEN 'NorthWest'
                            WHEN c.Region IN ('KwaZulu-Natal', 'KZN') THEN 'KwaZulu-Natal'
                            WHEN c.Region IN ('Gauteng', 'GT') THEN 'Gauteng'
                            WHEN c.Region IN ('NorthernCape', 'NC') THEN 'NorthernCape'
                            WHEN c.Region IN ('Mpumalanga', 'MP') THEN 'Mpumalanga'
                            WHEN c.Region IN ('Limpopo', 'LP') THEN 'Limpopo'
                            ELSE c.Region
                        END AS Region,
                        COUNT(l.ApprovalStatus) AS RejectedApplications
                -- Join the customers and loans tables on CustomerID
                FROM customers c
                JOIN loans l
                ON c.CustomerID = l.CustomerID
                -- Filter for RejectedApplications
                WHERE l.ApprovalStatus = 'Rejected'
                -- Group by Region
                GROUP BY CASE
                            WHEN c.Region IN ('EasternCape', 'EC') THEN 'EasternCape'
                            WHEN c.Region IN ('FreeState', 'FS') THEN 'FreeState'
                            WHEN c.Region IN ('WesternCape', 'WC') THEN 'WesternCape'
                            WHEN c.Region IN ('NorthWest', 'NW') THEN 'NorthWest'
                            WHEN c.Region IN ('KwaZulu-Natal', 'KZN') THEN 'KwaZulu-Natal'
                            WHEN c.Region IN ('Gauteng', 'GT') THEN 'Gauteng'
                            WHEN c.Region IN ('NorthernCape', 'NC') THEN 'NorthernCape'
                            WHEN c.Region IN ('Mpumalanga', 'MP') THEN 'Mpumalanga'
                            WHEN c.Region IN ('Limpopo', 'LP') THEN 'Limpopo'
                            ELSE c.Region
                        END
            """

    return qry


def question_3():
    """
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    qry =   """
                -- Create the financing table
                CREATE TABLE financing AS
                -- Select the required columns from the customers, loans and credit tables
                SELECT cu.CustomerID, cu.Income, lo.LoanAmount, lo.LoanTerm, lo.InterestRate, lo.ApprovalStatus, cr.CreditScore
                -- Join the customers, loans and credit tables on CustomerID
                FROM customers cu
                JOIN loans lo
                ON cu.CustomerID = lo.CustomerID
                JOIN credit cr
                ON cu.CustomerID = cr.CustomerID
            """

    return qry


# Question 4 and 5 are linked


def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.
    """

    qry =   """
                -- Create the timeline table
                CREATE TABLE timeline AS
                -- Select the required columns from the customers, months and repayments tables
                SELECT c.CustomerID, m.MonthName, COUNT(r.RepaymentID) AS NumberOfRepayments, COALESCE(SUM(r.Amount), 0) AS AmountTotal
                -- Cross join the customers and months tables to get all possible combinations
                FROM customers c
                CROSS JOIN months m
                -- Left join the repayments table on CustomerID and MonthID
                LEFT JOIN repayments r
                ON c.CustomerID = r.CustomerID
                AND m.MonthID = strftime('%m', r.RepaymentDate)
                -- Filter for Repayments between 6am and 6pm London Time
                WHERE CASE
                        WHEN r.TimeZone = 'GMT' THEN strftime('%H', r.RepaymentDate) BETWEEN 6 AND 18
                        WHEN r.TimeZone = 'CAT' THEN strftime('%H', r.RepaymentDate) BETWEEN 7 AND 19
                        WHEN r.TimeZone = 'IST' THEN strftime('%H', r.RepaymentDate) BETWEEN 11 AND 23
                        WHEN r.TimeZone = 'JST' THEN strftime('%H', r.RepaymentDate) BETWEEN 15 AND 3
                        WHEN r.TimeZone = 'EET' THEN strftime('%H', r.RepaymentDate) BETWEEN 8 AND 20
                        WHEN r.TimeZone = 'PNT' THEN strftime('%H', r.RepaymentDate) BETWEEN 23 AND 11
                        WHEN r.TimeZone = 'CST' THEN strftime('%H', r.RepaymentDate) BETWEEN 0 AND 12
                        WHEN r.TimeZone = 'CET' THEN strftime('%H', r.RepaymentDate) BETWEEN 7 AND 19
                        WHEN r.TimeZone = 'UTC' THEN strftime('%H', r.RepaymentDate) BETWEEN 6 AND 18
                      END
                -- Group by CustomerID and MonthName
                GROUP BY c.CustomerID, m.MonthName
            """

    return qry


def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    qry =   """
                -- Pivot the timeline table to get the required columns for each month
                SELECT CustomerID,
                    CAST(SUM(CASE WHEN MonthName = 'January' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS JanuaryRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'January' THEN AmountTotal ELSE 0 END), 2) AS JanuaryTotal,
                    CAST(SUM(CASE WHEN MonthName = 'February' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS FebruaryRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'February' THEN AmountTotal ELSE 0 END), 2) AS FebruaryTotal,
                    CAST(SUM(CASE WHEN MonthName = 'March' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS MarchRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'March' THEN AmountTotal ELSE 0 END), 2) AS MarchTotal,
                    CAST(SUM(CASE WHEN MonthName = 'April' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS AprilRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'April' THEN AmountTotal ELSE 0 END), 2) AS AprilTotal,
                    CAST(SUM(CASE WHEN MonthName = 'May' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS MayRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'May' THEN AmountTotal ELSE 0 END), 2) AS MayTotal,
                    CAST(SUM(CASE WHEN MonthName = 'June' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS JuneRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'June' THEN AmountTotal ELSE 0 END), 2) AS JuneTotal,
                    CAST(SUM(CASE WHEN MonthName = 'July' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS JulyRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'July' THEN AmountTotal ELSE 0 END), 2) AS JulyTotal,
                    CAST(SUM(CASE WHEN MonthName = 'August' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS AugustRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'August' THEN AmountTotal ELSE 0 END), 2) AS AugustTotal,
                    CAST(SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS SeptemberRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'September' THEN AmountTotal ELSE 0 END), 2) AS SeptemberTotal,
                    CAST(SUM(CASE WHEN MonthName = 'October' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS OctoberRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'October' THEN AmountTotal ELSE 0 END), 2) AS OctoberTotal,
                    CAST(SUM(CASE WHEN MonthName = 'November' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS NovemberRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'November' THEN AmountTotal ELSE 0 END), 2) AS NovemberTotal,
                    CAST(SUM(CASE WHEN MonthName = 'December' THEN NumberOfRepayments ELSE 0 END) AS INTEGER) AS DecemberRepayments,
                    ROUND(SUM(CASE WHEN MonthName = 'December' THEN AmountTotal ELSE 0 END), 2) AS DecemberTotal
                FROM timeline
                -- Group by CustomerID
                GROUP BY CustomerID
            """

    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """

    qry =   """
                -- Create the corrected_customers table
                CREATE TABLE corrected_customers AS
                -- Select the required columns from the customers table
                SELECT 
                    CustomerID, 
                    Age, 
                    Gender,
                    LAG(Age, 2) OVER (PARTITION BY Gender ORDER BY CustomerID) AS CorrectedAge
                FROM customers
                -- Order by CustomerID
                ORDER BY CustomerID;

                -- Manually correct the NULL values that overflow
                UPDATE corrected_customers
                SET CorrectedAge = (SELECT Age FROM customers WHERE CustomerID = corrected_customers.CustomerID)
                WHERE CorrectedAge IS NULL;

                -- Return the corrected_customers table
                SELECT * FROM corrected_customers;
            """
    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """

    qry =   """
                -- Add the AgeCategory column to the corrected_customers table
                ALTER TABLE corrected_customers
                ADD COLUMN AgeCategory TEXT;

                -- Update the AgeCategory column based on the CorrectedAge
                UPDATE corrected_customers
                SET AgeCategory = CASE
                                    WHEN CorrectedAge < 20 THEN 'Teen'
                                    WHEN CorrectedAge >= 20 AND CorrectedAge < 30 THEN 'Young Adult'
                                    WHEN CorrectedAge >= 30 AND CorrectedAge < 60 THEN 'Adult'
                                    WHEN CorrectedAge >= 60 THEN 'Pensioner'
                                  END;

                -- Create a Common Table Expression to get the RepaymentCount per CustomerID
                WITH RepaymentCounts AS (
                    SELECT 
                        c.CustomerID, 
                        COUNT(r.RepaymentID) AS RepaymentCount
                    FROM 
                        corrected_customers c
                    LEFT JOIN 
                        repayments r ON c.CustomerID = r.CustomerID
                    GROUP BY 
                        c.CustomerID
                ),
                -- Create a Common Table Expression to rank the customers based on RepaymentCount
                RankedCustomers AS (
                    SELECT 
                        c.CustomerID, 
                        c.Age, 
                        c.CorrectedAge, 
                        c.Gender, 
                        c.AgeCategory, 
                        RepaymentCount,
                        RANK() OVER (PARTITION BY c.AgeCategory ORDER BY RepaymentCount DESC) AS Rank
                    FROM 
                        corrected_customers c
                    LEFT JOIN 
                        RepaymentCounts rc ON c.CustomerID = rc.CustomerID
                )
                -- Return the required columns from the RankedCustomers table
                SELECT 
                    CustomerID, 
                    Age, 
                    CorrectedAge, 
                    Gender, 
                    AgeCategory, 
                    Rank
                FROM 
                    RankedCustomers;
            """

    return qry

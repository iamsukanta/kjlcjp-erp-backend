from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.income import Income
from app.models.cost import Cost


async def get_dashboard_statistics(db: AsyncSession):
    # Income
    income_query = select(
        Income.income_type,
        func.coalesce(func.sum(Income.amount), 0)
    ).group_by(Income.income_type)
    income_result = await db.execute(income_query)
    income_data = dict(income_result.all())

    # Cost
    cost_query = select(
        Cost.cost_type,
        func.coalesce(func.sum(Cost.amount), 0)
    ).group_by(Cost.cost_type)
    cost_result = await db.execute(cost_query)
    cost_data = dict(cost_result.all())
    
    income_company = income_data.get("company", 0)
    income_school = income_data.get("school", 0)
    cost_company = cost_data.get("company", 0)
    cost_school = cost_data.get("school", 0)

    return {
        "totalCompanyIncome": income_company,
        "totalCompanyCost": cost_company,
        "totalCompanyProfit": income_company - cost_company,
        "totalSchoolCost": cost_school,
        "totalSchoolIncome": income_school,
        "totalSchoolProfit": income_school - cost_school
    }



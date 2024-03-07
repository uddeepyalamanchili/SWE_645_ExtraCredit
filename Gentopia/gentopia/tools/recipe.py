from typing import AnyStr
import requests
import random
from bs4 import BeautifulSoup
from gentopia.tools.basetool import *
class GetRecipeIDArgs(BaseModel):
    main_item: str = Field(..., description="main item in the recipe")

class GetRecipeID(BaseTool):
    name = "get_recipe_id"
    description="A tool to find the id of recipe based on given main ingredient"
    args_schema: Optional[Type[BaseModel]] = GetRecipeIDArgs

    def _run(self, main_item: AnyStr) -> str:
        try:
            url = "https://www.themealdb.com/api/json/v1/1/filter.php?i="+main_item
            res = requests.get(url)
            res = res.json()
            ids = []
            for i in range(len(res['meals'])):
                ids.append(res['meals'][i]['idMeal'])
            return random.choice(ids)
        except:
            print("Something wrong with fetching id or that major item based recipes not available")
            return "Something wrong with fetching id or that major item based recipes not available"
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
class RecipeGeneratorArgs(BaseModel):
    id: str = Field(..., description ="Id of the recipe generator")

class RecipeGenerator(BaseTool):
    """Tool that adds the capability to query the Google search API."""

    name ="get_recipe_by_id"
    description = "A tool to retrieve web pages through url. Useful when you have a url and need to find detailed information inside."

    args_schema: Optional[Type[BaseModel]] = RecipeGeneratorArgs

    def _run(self, id: str) -> str:
        try:
            url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i="+id
            response = requests.get(url)
            return response.json()['meals'][0]['strInstructions']

        except Exception as e:
            return f"Error: {e}\n Probably it is an invalid URL."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = GetRecipeID("chicken_breast")
    ans = RecipeGenerator(ans)
    print(ans)

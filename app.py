from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import RedirectResponse
from routers.dreamina import DreaminaImage, DreaminaTextToVideo, DreaminaImageToVideo

# 初始化核心应用
app = FastAPI(
    title="Volcengine FASTAPI代理",
    description="Volcengine FASTAPI代理服务",
    version="1.0.0",
)

# 根路径重定向到docs
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由模块
from routers import health, image, task , V2TextToImage

app.include_router(image.router, prefix="/volcengine")
app.include_router(task.router, prefix="/volcengine")
app.include_router(V2TextToImage.router, prefix="/volcengine")

app.include_router(DreaminaImage.router, prefix="/volcengine", tags=["Dreamina"])
app.include_router(DreaminaTextToVideo.router, prefix="/volcengine", tags=["Dreamina"])
app.include_router(DreaminaImageToVideo.router, prefix="/volcengine", tags=["Dreamina"])
app.include_router(health.router)

# 启动服务
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5002, reload=True)
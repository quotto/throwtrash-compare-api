FROM throwtrash/compare:prebuild

# FUNCTION_DIRはprebuildコンテナで設定
WORKDIR ${FUNCTION_DIR}
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler.lambda_handler" ]
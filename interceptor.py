import grpc
import jwt


def _abort(code, details):

    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class AuthenticationInterceptor:
    def __init__(self, secret_key, algorithm):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._terminator = _abort(
            grpc.StatusCode.UNAUTHENTICATED, "Unauthorized")

    def intercept_service(self, continuation, handler_call_details):
        """
        拦截器函数，根据业务处理判断，返回对应的函数
        :param continuation: 函数执行器
        :param handler_call_details: 客户端传来的header
        :return:
        """

        # print(continuation)
        headers = dict(handler_call_details.invocation_metadata)
        token = headers.get("authorization", "").split("Bearer ")[-1]
        try:
            # 验证 JWT
            decoded_token = jwt.decode(
                token, self._secret_key, algorithms=[self._algorithm])

            # 进行其他身份验证逻辑，例如检查用户权限等
            print(decoded_token)

            # 调用下一个方法处理程序
            return continuation(handler_call_details)
        except Exception as e:
            # 如果身份验证失败，则返回错误
            return self._terminator

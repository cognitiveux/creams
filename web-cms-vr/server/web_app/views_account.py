from .views import *

class AccountMgmtActivateAccount(GenericAPIView):
    """
    post:
    Activates the account if the provided verification code matches the latest verification code received via email.
    """
    serializer_class = AccountMgmtActivateAccountSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['resource_is_activated', 'user'],
        ['bad_request'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtActivateAccount', response_types)

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            log.debug("{} START".format(request_details(request)))
            serialized_request = serialize_request(request)
            serialized_item = AccountMgmtActivateAccountSerializer(data=req_data)
            is_resource_activated = False

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        email = req_data.get('email')
                        received_verification_code = req_data.get('verification_code')
                        ts_now = now()
                        user_row = Users.objects.filter(email=email).values('id')

                        if not user_row:
                            raise ApplicationError(['resource_not_found', 'user'])

                        user_fk_id = user_row[0].get('id')
                        active_user_row = ActiveUsers.objects.filter(user_fk_id=user_fk_id).values('verification_code', 'ts_activation')
                        stored_verification_code = active_user_row[0].get('verification_code')
                        stored_ts_activation = active_user_row[0].get('ts_activation')

                        # First time the account gets activated
                        if stored_verification_code == received_verification_code and not stored_ts_activation:
                            log.debug("{} Verification codes match.".format(request_details(request)))
                            ActiveUsers.objects.filter(
                                user_fk_id=user_fk_id
                            ).update(
                                ts_activation=ts_now
                            )
                            is_resource_activated = True
                        # Check if the account is already activated
                        elif stored_ts_activation:
                            log.debug("{} Account is already activated {}".format(request_details(request), email))
                            is_resource_activated = True
                        else:
                            log.debug("{} Verification codes mismatch.".format(request_details(request)))
                            is_resource_activated = False
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response

                    status_code, message = get_code_and_response(['resource_is_activated', 'user'])
                    content = {}
                    content[MESSAGE] = message
                    content[RESOURCE_NAME] = 'user'
                    content[RESOURCE_IS_ACTIVATED] = is_resource_activated
                    response = {}
                    response[CONTENT] = content
                    response[STATUS_CODE] = status_code
                    log.debug("{} SUCCESS".format(request_details(request)))
                    data = response
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to activate account."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtCreateUser(CreateAPIView):
    """
    post:
    Creates a new user instance
    """
    serializer_class = AccountMgmtCreateUserSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtCreateUser', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def send_registration_email_task(self, email, verification_code, verification_type):
        send_verification_email(email, verification_code, verification_type)


    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AccountMgmtCreateUserSerializer(data=req_data)

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        email = req_data.get('email')
                        name = req_data.get('name')
                        organization = req_data.get('organization')
                        password = req_data.get('password')
                        role = req_data.get('role')
                        surname = req_data.get('surname')
                        password_hash = make_password(password)
                        ts_now = now()
                        class_lvl = req_data.get('class_level')

                        user = Users(
                            email=email,
                            name=name,
                            organization=organization,
                            password=password_hash,
                            role=role,
                            surname=surname,
                            ts_entry_added=ts_now,
                            ts_last_updated=ts_now,
                            class_level = class_lvl,
                        )
                        user.save()

                        verification_code = generate_random_uuid()
                        user_row = Users.objects.filter(email=email).values('id')
                        user_fk_id = user_row[0].get('id')

                        ActiveUsers.objects.update_or_create(
                            user_fk_id=user_fk_id,
                            defaults={
                                'verification_code': verification_code,
                                'frequent_request_count': 1,
                                'ts_added': ts_now,
                            }
                        )

                        # Send email in the background after ``countdown`` seconds and return success
                        result = self.send_registration_email_task.apply_async(
                            (email, verification_code, 'ACCOUNT'),
                            countdown=settings.EMAIL_COUNTDOWN_SEC
                        )
                        Users.objects.filter(email=email).update(c_register_task_id=result.id)
                        log.debug("{} Will send registration email to: {}. Updating async result with task ID: {}".format(
                                request_details(request), email, result.id
                            )
                        )
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'user'
                        response = {}
                        response[CONTENT] = content
                        response[STATUS_CODE] = status_code
                        log.debug("{} SUCCESS".format(request_details(request)))
                        data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to register user."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtLogin(TokenObtainPairView):
    """
    post: Creates a JSON Web Token if the provided credentials are correct
    """
    serializer_class = AccountMgmtLoginSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['resource_created_return_obj', 'jwt'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_activated', 'user'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtLogin', response_types)

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            log.debug("{} START".format(request_details(request)))
            log.debug("{} Requested login email: {}".format(request_details(request), req_data.get('email')))
            status_code, tokens = AccountMgmtLoginSerializer(req_data).validate(req_data)
            response[CONTENT] = tokens
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            data = response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            data = response
            return Response(data[CONTENT], status=data[STATUS_CODE])
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to login."
            }
            return Response(content, status=status_code)

        to_return = Response(data[CONTENT], status=data[STATUS_CODE])
        #FIXME add secure=True when HTTP certificate issue is resolved
        to_return.set_cookie('access_tkn', data['content']['resource_obj']['access'],  httponly=True)
        to_return.set_cookie('refresh_tkn', data['content']['resource_obj']['refresh'],   httponly=True)
        return to_return


class AccountMgmtPollResetEmailStatus(GenericAPIView):
    """
    get:
    Polls the status of the reset code ``email``.
    """
    serializer_class = AccountMgmtPollResetEmailStatusSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success_with_status_return'],
        ['bad_request'],
        ['resource_not_found', 'c_reset_task_id'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtPollResetEmailStatus', response_types)
    email_param = openapi.Parameter(
        'email',
        in_=openapi.IN_QUERY,
        description='Email',
        type=openapi.TYPE_STRING,
        required=True,
    )

    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters=[email_param]
    )
    def get(self, request):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AccountMgmtPollResetEmailStatusSerializer(data=req_data)

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                try:
                    log.debug("{} VALID DATA".format(request_details(request)))
                    email = req_data.get('email')
                    user_row = Users.objects.filter(email=email).values('c_reset_task_id')

                    if not user_row:
                        raise ApplicationError(['resource_not_found', 'user'])

                    c_reset_task_id = user_row[0].get('c_reset_task_id')
                    result = AsyncResult(c_reset_task_id)

                    if not c_reset_task_id or not result:
                        raise ApplicationError(['resource_not_found', 'c_reset_task_id'])

                    c_task_status = "PENDING"

                    if result.state == 'PENDING':
                        c_task_status = "PENDING"
                    elif result.state == "FAILURE":
                        c_task_status = "FAILURE"
                    elif result.state == 'SUCCESS':
                        c_task_status = "SUCCESS"

                    status_code, message = get_code_and_response(['success_with_status_return'])
                    content = {}
                    content[MESSAGE] = message
                    content[TASK_STATUS] = c_task_status
                    response = {}
                    response[CONTENT] = content
                    response[STATUS_CODE] = status_code
                    log.debug("{} SUCCESS".format(request_details(request)))
                    data = response
                except ApplicationError as e:
                    log.info("{} ERROR: {}".format(request_details(request), str(e)))
                    response = {}
                    log.info("e.get_response_body(): {}".format(e.get_response_body()))
                    log.info("e.status_code: {}".format(e.status_code))
                    response[CONTENT] = e.get_response_body()
                    response[STATUS_CODE] = e.status_code
                    data = response

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to poll reset code email status."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtPollVerificationEmailStatus(GenericAPIView):
    """
    get:
    Polls the status of the registration ``email`` for account verification.
    """
    serializer_class = AccountMgmtPollVerificationEmailStatusSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success_with_status_return'],
        ['bad_request'],
        ['resource_not_found', 'c_register_task_id'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtPollVerificationEmailStatus', response_types)
    email_param = openapi.Parameter(
        'email',
        in_=openapi.IN_QUERY,
        description='Email',
        type=openapi.TYPE_STRING,
        required=True,
    )

    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters=[email_param]
    )
    def get(self, request):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AccountMgmtPollVerificationEmailStatusSerializer(data=req_data)

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                try:
                    log.debug("{} VALID DATA".format(request_details(request)))
                    email = req_data.get('email')
                    user_row = Users.objects.filter(email=email).values('c_register_task_id')

                    if not user_row:
                        raise ApplicationError(['resource_not_found', 'user'])

                    c_register_task_id = user_row[0].get('c_register_task_id')
                    result = AsyncResult(c_register_task_id)

                    if not c_register_task_id or not result:
                        raise ApplicationError(['resource_not_found', 'c_register_task_id'])

                    c_task_status = "PENDING"

                    if result.state == 'PENDING':
                        c_task_status = "PENDING"
                    elif result.state == "FAILURE":
                        c_task_status = "FAILURE"
                    elif result.state == 'SUCCESS':
                        c_task_status = "SUCCESS"

                    status_code, message = get_code_and_response(['success_with_status_return'])
                    content = {}
                    content[MESSAGE] = message
                    content[TASK_STATUS] = c_task_status
                    response = {}
                    response[CONTENT] = content
                    response[STATUS_CODE] = status_code
                    log.debug("{} SUCCESS".format(request_details(request)))
                    data = response
                except ApplicationError as e:
                    log.info("{} ERROR: {}".format(request_details(request), str(e)))
                    response = {}
                    log.info("e.get_response_body(): {}".format(e.get_response_body()))
                    log.info("e.status_code: {}".format(e.status_code))
                    response[CONTENT] = e.get_response_body()
                    response[STATUS_CODE] = e.status_code
                    data = response

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to poll registration email status."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtRefreshToken(TokenRefreshView):
    """
    post: Uses the longer-lived refresh token to obtain another access token
    """
    serializer_class = AccountMgmtRefreshTokenSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['resource_created_return_str', 'jwt'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtRefreshToken', response_types)

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            log.debug("{} SUCCESS".format(request_details(request)))
            status_code, token = AccountMgmtRefreshTokenSerializer(req_data).validate(req_data)
            response[CONTENT] = token
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            data = response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            data = response
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to refresh token."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtRequestAccountVerificationCode(GenericAPIView):
    """
    post:
    Request a verification code for account activation via email.
    """
    serializer_class = AccountMgmtRequestAccountVerificationCodeSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['resource_is_activated', 'user'],
        ['bad_request'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['request_limit_exceeded', 'user'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtRequestAccountVerificationCode', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def send_registration_email_task(self, email, verification_code, verification_type):
        send_verification_email(email, verification_code, verification_type)


    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AccountMgmtRequestAccountVerificationCodeSerializer(data=req_data)

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        email = req_data.get('email')
                        user_row = Users.objects.filter(email=email).values('id')

                        if not user_row:
                            raise ApplicationError(['resource_not_found', 'user'])

                        user_fk_id = user_row[0].get('id')
                        active_user_row = ActiveUsers.objects.filter(user_fk_id=user_fk_id).first()
                        is_resource_activated = False

                        if not active_user_row:
                            new_active_user_row = ActiveUsers(
                                user_fk_id=user_fk_id,
                                frequent_request_count=0,
                                ts_added=now(),
                            )
                            new_active_user_row.save()

                        active_user_row = ActiveUsers.objects.filter(user_fk_id=user_fk_id).first()

                        if active_user_row.ts_activation:
                            log.debug("{} Account is already activated. Email: {}".format(request_details(request), email))
                            is_resource_activated = True
                        else:
                            frequent_request_count = active_user_row.frequent_request_count
                            last_activation_request = active_user_row.ts_added
                            time_difference = now().timestamp() - last_activation_request.timestamp()
                            verification_type = 'ACCOUNT'
                            temp_object = __import__('web_app.models', fromlist=settings.MODEL_MAPPING[verification_type]['model_class'])
                            model_class = getattr(temp_object, settings.MODEL_MAPPING[verification_type]['model_class'])
                            resource_name = settings.MODEL_MAPPING[verification_type]['resource_name']

                            if frequent_request_count >= settings.FREQUENT_REQUEST_COUNT_LIMIT and time_difference < settings.ALLOWED_REQUEST_INTERVAL:
                                remaining_time = int((settings.ALLOWED_REQUEST_INTERVAL-time_difference)/60)
                                raise ApplicationError(['request_limit_exceeded', remaining_time], resource_name=resource_name+'_verification_code')
                            elif time_difference > settings.ALLOWED_REQUEST_INTERVAL:
                                frequent_request_count = 1
                            else:
                                frequent_request_count = (frequent_request_count+1)%settings.ALLOWED_REQUEST_INTERVAL

                            verification_code = generate_random_uuid()

                            ActiveUsers.objects.update_or_create(
                                user_fk_id=user_fk_id,
                                defaults={
                                    'verification_code': verification_code,
                                    'frequent_request_count': frequent_request_count,
                                    'ts_added': now(),
                                }
                            )

                            # Send email in the background after ``countdown`` seconds and return success
                            result = self.send_registration_email_task.apply_async(
                                (email, verification_code, verification_type),
                                countdown=settings.EMAIL_COUNTDOWN_SEC
                            )
                            Users.objects.filter(email=email).update(c_register_task_id=result.id)
                            log.debug("{} Will send registration email to: {}. Updating async result with task ID: {}".format(
                                    request_details(request), email, result.id
                                )
                            )

                        status_code, message = get_code_and_response(['resource_is_activated', 'user'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'user'
                        content[RESOURCE_IS_ACTIVATED] = is_resource_activated
                        response = {}
                        response[CONTENT] = content
                        response[STATUS_CODE] = status_code
                        log.debug("{} SUCCESS".format(request_details(request)))
                        data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to request account verification email."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtRequestPasswordResetCode(GenericAPIView):
    """
    post:
    Request a reset code for account reset password via email.
    """
    serializer_class = AccountMgmtRequestPasswordResetCodeSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['resource_not_activated', 'user'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['request_limit_exceeded', 'user'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtRequestPasswordResetCode', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def send_reset_code_email_task(self, email, verification_code, verification_type):
        send_verification_email(email, verification_code, verification_type)


    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AccountMgmtRequestPasswordResetCodeSerializer(data=req_data)

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        email = req_data.get('email')
                        user_row = Users.objects.filter(email=email).values('id')

                        if not user_row:
                            raise ApplicationError(['resource_not_found', 'user'])

                        user_fk_id = user_row[0].get('id')
                        active_user_row = ActiveUsers.objects.filter(user_fk_id=user_fk_id).first()

                        if not active_user_row.ts_activation:
                            raise ApplicationError(['resource_not_activated', 'user'])

                        reset_password_row = ResetPassword.objects.filter(user_fk_id=user_fk_id).first()

                        if not reset_password_row:
                            new_reset_password_row = ResetPassword(
                                user_fk_id=user_fk_id,
                                frequent_request_count=0,
                                ts_reset=None,
                            )
                            new_reset_password_row.save()

                        reset_password_row = ResetPassword.objects.filter(user_fk_id=user_fk_id).first()
                        frequent_request_count = reset_password_row.frequent_request_count
                        last_reset_request = reset_password_row.ts_requested
                        time_difference = now().timestamp() - last_reset_request.timestamp()

                        verification_type = 'RESET_PASSWORD'
                        temp_object = __import__('web_app.models', fromlist=settings.MODEL_MAPPING[verification_type]['model_class'])
                        model_class = getattr(temp_object, settings.MODEL_MAPPING[verification_type]['model_class'])
                        resource_name = settings.MODEL_MAPPING[verification_type]['resource_name']

                        if frequent_request_count >= settings.FREQUENT_REQUEST_COUNT_LIMIT and time_difference < settings.RESET_PASSWORD_INTERVAL:
                            remaining_time = int((settings.RESET_PASSWORD_INTERVAL-time_difference)/60)
                            raise ApplicationError(['request_limit_exceeded', remaining_time], resource_name=resource_name+'_verification_code')
                        elif time_difference > settings.RESET_PASSWORD_INTERVAL:
                            frequent_request_count = 1
                        else:
                            frequent_request_count = (frequent_request_count+1)%settings.RESET_PASSWORD_INTERVAL

                        verification_code = generate_random_uuid()

                        ResetPassword.objects.update_or_create(
                            user_fk_id=user_fk_id,
                            defaults={
                                'reset_code': verification_code,
                                'frequent_request_count': frequent_request_count,
                                'ts_expiration_reset': now()+timedelta(seconds=settings.RESET_PASSWORD_INTERVAL),
                                'ts_requested': now(),
                                'ts_reset': None,
                            }
                        )

                        # Send email in the background after ``countdown`` seconds and return success
                        result = self.send_reset_code_email_task.apply_async(
                            (email, verification_code, verification_type),
                            countdown=settings.EMAIL_COUNTDOWN_SEC
                        )
                        Users.objects.filter(email=email).update(c_reset_task_id=result.id)
                        log.debug("{} Will send reset code email to: {}. Updating async result with task ID: {}".format(
                                request_details(request), email, result.id
                            )
                        )

                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'user'
                        response = {}
                        response[CONTENT] = content
                        response[STATUS_CODE] = status_code
                        log.debug("{} SUCCESS".format(request_details(request)))
                        data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to request reset code via email."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtResetPassword(GenericAPIView):
    """
    post:
    Updates the password if the provided password reset code matches the latest password reset code received via email.
    """
    serializer_class = AccountMgmtResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['resource_not_activated', 'user'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['resource_expired', 'reset_code'],
        ['resource_incorrect', 'reset_code'],
        ['resource_not_requested', 'reset_code'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtResetPassword', response_types)

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AccountMgmtResetPasswordSerializer(data=req_data)
            is_resource_reset = False

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        email = req_data.get('email')
                        password = req_data.get('password')
                        received_reset_code = req_data.get('reset_code')
                        ts_now = now()
                        user_row = Users.objects.filter(email=email).values('id')

                        if not user_row:
                            raise ApplicationError(['resource_not_found', 'user'])

                        user_fk_id = user_row[0].get('id')
                        active_user_row = ActiveUsers.objects.filter(user_fk_id=user_fk_id).first()

                        if not active_user_row.ts_activation:
                            raise ApplicationError(['resource_not_activated', 'user'])

                        reset_password_row = ResetPassword.objects.filter(user_fk_id=user_fk_id).first()

                        if not reset_password_row:
                            log.debug("{} No active reset code.".format(request_details(request)))
                            raise ApplicationError(['resource_not_requested', 'reset_code'], reason='not_requested_reset_code')

                        active_reset_code = reset_password_row.reset_code
                        code_has_expired = reset_password_row.ts_expiration_reset.timestamp() < now().timestamp()

                        if not reset_password_row is None and active_reset_code == received_reset_code and not code_has_expired:
                            ts_now = now()
                            log.debug("{} Reset password codes match.".format(request_details(request)))
                            # set the expiration timestamp to now() to invalidate the current reset code
                            ResetPassword.objects.filter(user_fk_id=user_fk_id).update(
                                ts_reset=ts_now,
                                ts_expiration_reset=ts_now
                            )
                            password_hash = make_password(password)
                            Users.objects.filter(email=email).update(
                                password=password_hash
                            )
                            status_code, message = get_code_and_response(['success'])
                            content = {}
                            content[MESSAGE] = message
                            content[RESOURCE_NAME] = 'password'
                            response = {}
                            response[CONTENT] = content
                            response[STATUS_CODE] = status_code
                            log.debug("{} SUCCESS".format(request_details(request)))
                            data = response
                        elif active_reset_code != received_reset_code:
                            log.debug("{} Reset codes mismatch.".format(request_details(request)))
                            raise ApplicationError(['resource_incorrect', 'reset_code'], reason='incorrect_reset_code')
                        else:
                            log.debug("{} Reset code has expired.".format(request_details(request)))
                            raise ApplicationError(['resource_expired', 'reset_code'], reason='expired_reset_code')
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to reset password."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AccountMgmtUpdatePassword(GenericAPIView):
    """
    post:
    Updates the user's password.
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = AccountMgmtUpdatePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_activated', 'user'],
        ['resource_not_allowed', 'user'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['resource_incorrect', 'password'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AccountMgmtUpdatePassword', response_types)

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AccountMgmtUpdatePasswordSerializer(data=req_data)
            is_resource_reset = False

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        email = req_data.get('email')
                        current_password = req_data.get('current_password')
                        new_password = req_data.get('new_password')
                        ts_now = now()
                        user_row = Users.objects.filter(email=email).values('id', 'password')

                        if not user_row:
                            raise ApplicationError(['resource_not_found', 'user'])

                        user_fk_id = user_row[0].get('id')
                        active_user_row = ActiveUsers.objects.filter(user_fk_id=user_fk_id).first()

                        if not active_user_row.ts_activation:
                            raise ApplicationError(['resource_not_activated', 'user'])

                        encoded_jwt = request.headers['Authorization'].split('Bearer ')[1]
                        decoded_jwt = jwt.decode(
                            encoded_jwt,
                            settings.SIMPLE_JWT['SIGNING_KEY'],
                            settings.SIMPLE_JWT['ALGORITHM'],
                            audience=settings.SIMPLE_JWT['AUDIENCE']
                        )

                        if decoded_jwt.get('sub') != email:
                            raise ApplicationError(['resource_not_allowed', 'user'])

                        password_hash = user_row[0].get('password')

                        # Check if the existing password_hash is valid
                        if not check_password(current_password, password_hash):
                            log.debug("{} Password is incorrect".format(request_details(request)))
                            raise ApplicationError(['resource_incorrect', 'password'])
                        else:
                            new_password_hash = make_password(new_password)
                            Users.objects.filter(email=email).update(
                                password=new_password_hash
                            )
                            status_code, message = get_code_and_response(['success'])
                            content = {}
                            content[MESSAGE] = message
                            content[RESOURCE_NAME] = 'password'
                            response = {}
                            response[CONTENT] = content
                            response[STATUS_CODE] = status_code
                            log.debug("{} SUCCESS".format(request_details(request)))
                            data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to update password."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


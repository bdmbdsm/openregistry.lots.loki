# -*- coding: utf-8 -*-
from openregistry.lots.core.utils import (
    raise_operation_error,
    update_logging_context,
    get_now
)
from openregistry.lots.core.validation import (
    validate_data
)

def validate_document_operation_in_not_allowed_lot_status(request, error_handler, **kwargs):
    status = request.validated['lot_status']
    if status != 'pending':
        raise_operation_error(request, error_handler,
                              'Can\'t update document in current ({}) lot status'.format(status))


def validate_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context if 'items' in request.context else request.context.__parent__
    model = type(context).items.model_class
    validate_data(request, model)


def validate_publication_data(request, error_handler, **kwargs):
    update_logging_context(request, {'publication_id': '__new__'})
    context = request.context if 'publications' in request.context else request.context.__parent__
    model = type(context).publications.model_class
    validate_data(request, model)


def validate_decision_post(request, error_handler, **kwargs):
    if len(request.validated['lot'].decisions) > 1:
        raise_operation_error(request, error_handler,
                              'Can\'t add more than one decisions to lot')


def validate_decision_patch(request, error_handler, **kwargs):
    # Validate second decision because second decision come from asset and can be changed
    is_decisions_available = bool(
        len(request.context.decisions) == 2 or
        len(request.json['data'].get('decisions', [])) == 2
    )
    if request.json['data'].get('status') == 'pending' and not is_decisions_available:
        raise_operation_error(request, error_handler,
                                  'Can\'t switch to pending while decisions not available.')

    is_asset_decision_patched_wrong = bool(
        len(request.context.decisions) < 2 or
        (
            request.json['data'].get('decisions') and (
                len(request.json['data']['decisions']) < 2 or
                request.context.decisions[1].serialize() != request.json['data']['decisions'][1]
            )
        )
    )
    if request.context.status == 'pending' and is_asset_decision_patched_wrong:
        raise_operation_error(request, error_handler,
                                  'Can\'t update decision that was created from asset')


def rectificationPeriod_item_validation(request, error_handler, **kwargs):
    if request.validated['lot'].rectificationPeriod and request.validated['lot'].rectificationPeriod.endDate < get_now():
        request.errors.add('body', 'mode', 'You can\'t change items after rectification period')
        request.errors.status = 403
        raise error_handler(request)


def rectificationPeriod_document_validation(request, error_handler, **kwargs):
    is_period_ended = bool(
        request.validated['lot'].rectificationPeriod and
        request.validated['lot'].rectificationPeriod.endDate < get_now()
    )
    if (is_period_ended and request.validated['document'].documentType != 'cancellationDetails') and request.method == 'POST':
        request.errors.add('body', 'mode', 'You can add only document with cancellationDetails after rectification period')
        request.errors.status = 403
        raise error_handler(request)

    if is_period_ended and request.method in ['PUT', 'PATCH']:
        request.errors.add('body', 'mode', 'You can\'t change documents after rectification period')
        request.errors.status = 403
        raise error_handler(request)


def validate_deleted_status(request, error_handler, **kwargs):
    can_be_deleted = any([doc.documentType == 'cancellationDetails' for doc in request.context['documents']])
    if request.json['data'].get('status') == 'deleted' and not can_be_deleted:
        request.errors.add(
            'body',
            'mode',
            "You can set deleted status"
            "only when asset have at least one document with \'cancellationDetails\' documentType")
        request.errors.status = 403
        raise error_handler(request)

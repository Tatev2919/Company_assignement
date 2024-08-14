import io

def stream_payments(callback_fn):
    """
    Reads payments from a payment processor and calls `callback_fn(amount)`
    for each payment.
    Returns when there is no more payments.
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in range(10):
        callback_fn(i)

# This is a library function, you can't modify it.
def store_payments(amount_iterator):
    """
    Iterates over the payment amounts from amount_iterator
    and stores them to a remote system.
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in amount_iterator:
        print(i)

def process_payments_2():
    def payment_generator():
        payments = []
        
        def callback_fn(amount):
            payments.append(amount)
        
        stream_payments(callback_fn)
        
        for payment in payments:
            yield payment

    generator = payment_generator()
    
    store_payments(generator)

process_payments_2()

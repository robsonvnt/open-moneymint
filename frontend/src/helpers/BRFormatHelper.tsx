export const formatDate = (date: Date): string => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return date.toLocaleDateString('pt-BR', options);
};

export const formatDateStr = (dateString: string): string => {
    return formatDate(new Date(dateString));
};

export const currencyFormatter = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
});

export const clearFloatFormatter = new Intl.NumberFormat('pt-BR', {

});
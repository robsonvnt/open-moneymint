export const formatDate = (date: Date): string => {
    const options: Intl.DateTimeFormatOptions = {year: 'numeric', month: '2-digit', day: '2-digit'};
    return date.toLocaleDateString('pt-BR', options);
};

export const formatMonth = (date: Date): string => {
    const ano = date.getFullYear();
    const mes = (date.getMonth() + 1).toString().padStart(2, '0'); // +1 porque os meses são zero-based
    return `${ano}-${mes}`;
};

export const formatDateStr = (dateString: string): string => {
    const sd = dateString.split("-")
    return `${sd[2]}/${sd[1]}/${sd[0]}`
};

export const currencyFormatter = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
});

export const clearFloatFormatter = new Intl.NumberFormat('pt-BR', {});
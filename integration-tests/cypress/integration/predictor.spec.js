describe('match predictor', () => {
    it('compare two teams', () => {
        cy.visit('http://localhost:3010');

        cy.contains('Match Predictor').should('exist');

        cy.get('#home-country').select('england')
        cy.get('#home-team').select('Chelsea')

        cy.get('#away-country').select('italy')
        cy.get('#away-team').select('AS Roma')

        cy.contains('Submit').click()

        cy.contains('AWAY').should('exist')
    });
});
